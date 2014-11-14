"use strict"

module.exports = createKDTree
module.exports.deserialize = deserializeKDTree

var ndarray = require("ndarray")
var ndselect = require("ndarray-select")
var pack = require("ndarray-pack")
var ops = require("ndarray-ops")
var ndscratch = require("ndarray-scratch")
var pool = require("typedarray-pool")
var inorderTree = require("inorder-tree-layout")
var bits = require("bit-twiddle")
var KDTHeap = require("./lib/heap.js")

function KDTree(points, ids, n, d) {
  this.points = points
  this.ids = ids
  this.dimension = d
  this.length = n
}

var proto = KDTree.prototype

proto.serialize = function() {
  if(this.length > 0) {
    return {
      p: Array.prototype.slice.call(this.points.data, 0, this.length*this.dimension),
      i: Array.prototype.slice.call(this.ids, 0, this.length)
    }
  } else {
    return { d: this.dimension }
  }
}

//Range query
proto.range = function kdtRangeQuery(lo, hi, visit) {
  var n = this.length
  if(n < 1) {
    return
  }

  //Check degenerate case
  var d = this.dimension
  for(var i=0; i<d; ++i) {
    if(hi[i] < lo[i]) {
      return
    }
  }

  var points = this.points
  var ids = this.ids

  //Walk tree in level order, skipping subtrees which do not intersect range
  var visitRange = ndscratch.malloc([n, 2, d])
  var visitIndex = pool.mallocInt32(n)
  var rangeData = visitRange.data
  var pointData = points.data
  var visitCount = 1
  var visitTop = 0
  var retval

  visitIndex[0] = 0
  pack(lo, visitRange.pick(0,0))
  pack(hi, visitRange.pick(0,1))
  
  while(visitTop < visitCount) {
    var idx = visitIndex[visitTop]
    var k = bits.log2(idx+1)%d
    var loidx = visitRange.index(visitTop, 0, 0)
    var hiidx = visitRange.index(visitTop, 1, 0)
    var pidx = points.index(idx, 0)

    var visitPoint = true
    for(var i=0; i<d; ++i) {
      var pc = pointData[pidx+i]
      if((pc < rangeData[loidx + i]) || 
         (rangeData[hiidx + i] < pc)) {
        visitPoint = false
        break
      }
    }
    if(visitPoint) {
      retval = visit(ids[idx])
      if(retval !== undefined) {
        break
      }
    }

    //Visit children
    var pk = pointData[pidx+k]
    var hk = rangeData[hiidx+k]
    var lk = rangeData[loidx+k]
    if(lk <= pk) {
      var left = 2 * idx + 1
      if(left < n) {
        visitIndex[visitCount] = left
        var y = visitRange.index(visitCount, 0, 0)
        for(var i=0; i<d; ++i) {
          rangeData[y+i] = rangeData[loidx+i]
        }
        var z = visitRange.index(visitCount, 1, 0)
        for(var i=0; i<d; ++i) {
          rangeData[z+i] = rangeData[hiidx+i]
        }
        rangeData[z+k] = Math.min(hk, pk)
        visitCount += 1
      }
    }
    if(pk <= hk) {
      var right = 2 * (idx + 1)
      if(right < n) {
        visitIndex[visitCount] = right
        var y = visitRange.index(visitCount, 0, 0)
        for(var i=0; i<d; ++i) {
          rangeData[y+i] = rangeData[loidx+i]
        }
        var z = visitRange.index(visitCount, 1, 0)
        for(var i=0; i<d; ++i) {
          rangeData[z+i] = rangeData[hiidx+i]
        }
        rangeData[y+k] = Math.max(lk, pk)
        visitCount += 1
      }
    }

    //Increment pointer
    visitTop += 1
  }
  ndscratch.free(visitRange)
  pool.free(visitIndex)
  return retval
}

proto.rnn = function(point, radius, visit) {
  if(radius < 0) {
    return
  }
  var n = this.length
  if(n < 1) {
    return
  }
  var d = this.dimension
  var points = this.points
  var ids = this.ids

  //Walk tree in level order, skipping subtrees which do not intersect sphere
  var visitDistance = ndscratch.malloc([n, d])
  var visitIndex = pool.mallocInt32(n)
  var distanceData = visitDistance.data
  var pointData = points.data
  var visitCount = 1
  var visitTop = 0
  var r2 = radius*radius
  var retval

  //Initialize top of queue
  visitIndex[0] = 0
  for(var i=0; i<d; ++i) {
    visitDistance.set(0, i, 0)
  }

  //Walk over queue
  while(visitTop < visitCount) {
    var idx = visitIndex[visitTop]
    var pidx = points.index(idx, 0)

    //Check if point in sphere
    var d2 = 0.0
    for(var i=0; i<d; ++i) {
      d2 += Math.pow(point[i] - pointData[pidx+i], 2)
    }
    if(d2 <= r2) {
      retval = visit(ids[idx])
      if(retval !== undefined) {
        break
      }
    }

    //Visit children
    var k = bits.log2(idx+1)%d
    var ds = 0.0
    var didx = visitDistance.index(visitTop, 0)
    for(var i=0; i<d; ++i) {
      if(i !== k) {
        ds += distanceData[didx + i]
      }
    }

    //Handle split axis
    var qk = point[k]
    var pk = pointData[pidx+k]
    var dk = distanceData[didx+k]
    var lk = dk
    var hk = dk
    if(qk < pk) {
      hk = Math.max(dk, Math.pow(pk - qk, 2))
    } else {
      lk = Math.max(dk, Math.pow(pk - qk, 2))
    }

    var d2l = lk + ds
    var d2h = hk + ds

    if(d2l <= r2) {
      var left = 2 * idx + 1
      if(left < n) {
        visitIndex[visitCount] = left
        var y = visitDistance.index(visitCount, 0)
        for(var i=0; i<d; ++i) {
          distanceData[y+i] = distanceData[didx+i]
        }
        distanceData[y+k] = lk
        visitCount += 1
      }
    }
    if(d2h <= r2) {
      var right = 2 * (idx + 1)
      if(right < n) {
        visitIndex[visitCount] = right
        var y = visitDistance.index(visitCount, 0)
        for(var i=0; i<d; ++i) {
          distanceData[y+i] = distanceData[didx+i]
        }
        distanceData[y+k] = hk
        visitCount += 1
      }
    }

    //Increment pointer
    visitTop += 1
  }

  ndscratch.free(visitDistance)
  pool.free(visitIndex)
  return retval
}

proto.nn = function(point, maxDistance) {
  var n = this.length
  if(n < 1) {
    return -1
  }
  if(typeof maxDistance === "number") {
    if(maxDistance < 0) {
      return -1
    } 
  } else {
    maxDistance = Infinity
  }
  var d = this.dimension
  var points = this.points
  var pointData = points.data
  var dataVector = pool.mallocFloat64(d)

  var toVisit = new KDTHeap(n, d+1)
  var index = toVisit.index
  var data = toVisit.data
  index[0] = 0
  for(var i=0; i<=d; ++i) {
    data[i] = 0
  }
  toVisit.count += 1

  var nearest = -1
  var nearestD = maxDistance

  while(toVisit.count > 0) {
    if(data[0] >= nearestD) {
      break
    }

    var idx = index[0]
    var pidx = points.index(idx, 0)
    var d2 = 0.0
    for(var i=0; i<d; ++i) {
      d2 += Math.pow(point[i]-pointData[pidx+i], 2)
    }
    if(d2 < nearestD) {
      nearestD = d2
      nearest = idx
    }

    //Compute distance bounds for children
    var k = bits.log2(idx+1)%d
    var ds = 0
    for(var i=0; i<d; ++i) {
      var dd = data[i+1]
      if(i !== k) {
        ds += dd
      }
      dataVector[i] = dd
    }
    var qk = point[k]
    var pk = pointData[pidx+k]
    var dk = dataVector[k]
    var lk = dk
    var hk = dk
    if(qk < pk) {
      hk = Math.max(dk, Math.pow(pk - qk, 2))
    } else {
      lk = Math.max(dk, Math.pow(pk - qk, 2))
    }
    var d2l = lk + ds
    var d2h = hk + ds

    toVisit.pop()
    
    if(d2l < nearestD) {
      var left = 2 * idx + 1
      if(left < n) {
        var vcount = toVisit.count
        index[vcount] = left
        var vptr = vcount * (d+1)
        data[vptr] = d2l
        for(var i=1; i<=d; ++i) {
          data[vptr+i] = dataVector[i-1]
        }
        data[vptr+k+1] = lk
        toVisit.push()
      }
    }
    if(d2h < nearestD) {
      var right = 2 * (idx + 1)
      if(right < n) {
        var vcount = toVisit.count
        index[vcount] = right
        var vptr = vcount * (d+1)
        data[vptr] = d2h
        for(var i=1; i<=d; ++i) {
          data[vptr+i] = dataVector[i-1]
        }
        data[vptr+k+1] = hk
        toVisit.push()
      }
    }
  }

  pool.freeFloat64(dataVector)
  toVisit.dispose()
  
  if(nearest < 0) {
    return -1
  }
  return this.ids[nearest]
}

proto.knn = function(point, maxPoints, maxDistance) {
  //Check degenerate cases
  if(typeof maxDistance === "number") {
    if(maxDistance < 0) {
      return []
    }
  } else {
    maxDistance = Infinity
  }
  var n = this.length
  if(n < 1) {
    return []
  }
  if(typeof maxPoints === "number") {
    if(maxPoints <= 0) {
      return []
    }
    maxPoints = Math.min(maxPoints, n)|0
  } else {
    maxPoints = n
  }
  var ids = this.ids

  var d = this.dimension
  var points = this.points
  var pointData = points.data
  var dataVector = pool.mallocFloat64(d)
  
  //List of closest points
  var closestPoints = new KDTHeap(maxPoints, 1)
  var cl_index = closestPoints.index
  var cl_data = closestPoints.data

  var toVisit = new KDTHeap(n, d+1)
  var index = toVisit.index
  var data = toVisit.data
  index[0] = 0
  for(var i=0; i<=d; ++i) {
    data[i] = 0
  }
  toVisit.count += 1

  var nearest = -1
  var nearestD = maxDistance

  while(toVisit.count > 0) {
    if(data[0] >= nearestD) {
      break
    }

    var idx = index[0]
    var pidx = points.index(idx, 0)
    var d2 = 0.0
    for(var i=0; i<d; ++i) {
      d2 += Math.pow(point[i]-pointData[pidx+i], 2)
    }
    if(d2 < nearestD) {
      if(closestPoints.count >= maxPoints) {
        closestPoints.pop()
      }
      var pcount = closestPoints.count
      cl_index[pcount] = idx
      cl_data[pcount] = -d2
      closestPoints.push()
      if(closestPoints.count >= maxPoints) {
        nearestD = -cl_data[0]
      }
    }

    //Compute distance bounds for children
    var k = bits.log2(idx+1)%d
    var ds = 0
    for(var i=0; i<d; ++i) {
      var dd = data[i+1]
      if(i !== k) {
        ds += dd
      }
      dataVector[i] = dd
    }
    var qk = point[k]
    var pk = pointData[pidx+k]
    var dk = dataVector[k]
    var lk = dk
    var hk = dk
    if(qk < pk) {
      hk = Math.max(dk, Math.pow(pk - qk, 2))
    } else {
      lk = Math.max(dk, Math.pow(pk - qk, 2))
    }
    var d2l = lk + ds
    var d2h = hk + ds

    toVisit.pop()
    if(d2l < nearestD) {
      var left = 2 * idx + 1
      if(left < n) {
        var vcount = toVisit.count
        index[vcount] = left
        var vptr = vcount * (d+1)
        data[vptr] = d2l
        for(var i=1; i<=d; ++i) {
          data[vptr+i] = dataVector[i-1]
        }
        data[vptr+k+1] = lk
        toVisit.push()
      }
    }
    if(d2h < nearestD) {
      var right = 2 * (idx + 1)
      if(right < n) {
        var vcount = toVisit.count
        index[vcount] = right
        var vptr = vcount * (d+1)
        data[vptr] = d2h
        for(var i=1; i<=d; ++i) {
          data[vptr+i] = dataVector[i-1]
        }
        data[vptr+k+1] = hk
        toVisit.push()
      }
    }
  }

  pool.freeFloat64(dataVector)
  toVisit.dispose()

  //Sort result
  var result = new Array(closestPoints.count)
  var ids = this.ids
  for(var i=closestPoints.count-1; i>=0; --i) {
    result[i] = ids[cl_index[0]]
    closestPoints.pop()
  }
  closestPoints.dispose()

  return result
}

proto.dispose = function kdtDispose() {
  pool.free(this.points.data)
  pool.freeInt32(this.ids)
  this.points = null
  this.ids = null
  this.length = 0
}

function createKDTree(points) {
  var n, d, indexed
  if(Array.isArray(points)) {
    n = points.length
    if(n === 0) {
      return new KDTree(null, null, 0, 0)
    }
    d = points[0].length
    indexed = ndarray(pool.mallocDouble(n*(d+1)), [n, d+1])
    pack(points, indexed.hi(n, d))
  } else {
    n = points.shape[0]
    d = points.shape[1]

    //Round up data type size
    var type = points.dtype
    if(type === "int8" ||
       type === "int16" ||
       type === "int32" ) {
      type = "int32"
    } else if(type === "uint8" ||
      type === "uint8_clamped" ||
      type === "buffer" ||
      type === "uint16" ||
      type === "uint32") {
      type = "uint32"
    } else if(type === "float32") {
      type = "float32"
    } else {
      type = "float64"
    }
    indexed = ndarray(pool.malloc(n*(d+1)), [n, d+1])
    ops.assign(indexed.hi(n,d), points)
  }
  for(var i=0; i<n; ++i) {
    indexed.set(i, d, i)
  }

  var pointArray = ndscratch.malloc([n, d], points.dtype)
  var indexArray = pool.mallocInt32(n)
  var pointer = 0
  var pointData = pointArray.data
  var arrayData = indexed.data
  var l2_n = bits.log2(bits.nextPow2(n))

  var sel_cmp = ndselect.compile(indexed.order, true, indexed.dtype)

  //Walk tree in level order
  var toVisit = [indexed]
  while(pointer < n) {
    var head = toVisit.shift()
    var array = head
    var nn = array.shape[0]|0
    
    //Find median
    if(nn > 1) {
      var k = bits.log2(pointer+1)%d
      var median
      var n_2 = inorderTree.root(nn)
      median = sel_cmp(array, n_2, function(a,b) {
        return a.get(k) - b.get(k)
      })

      //Copy into new array
      var pptr = pointArray.index(pointer, 0)
      var mptr = median.offset
      for(var i=0; i<d; ++i) {
        pointData[pptr++] = arrayData[mptr++]
      }
      indexArray[pointer] = arrayData[mptr]
      pointer += 1

      //Queue new items
      toVisit.push(array.hi(n_2))
      if(nn > 2) {
        toVisit.push(array.lo(n_2+1))
      }
    } else {
      //Copy into new array
      var mptr = array.offset
      var pptr = pointArray.index(pointer, 0)
      for(var i=0; i<d; ++i) {
        pointData[pptr+i] = arrayData[mptr++]
      }
      indexArray[pointer] = arrayData[mptr]
      pointer += 1
    }
  }

  //Release indexed
  pool.free(indexed.data)

  return new KDTree(pointArray, indexArray, n, d)
}

function deserializeKDTree(data) {
  var points = data.p
  var ids = data.i
  if(points) {
    var nd = points.length
    var pointArray = pool.mallocFloat64(nd)
    for(var i=0; i<nd; ++i) {
      pointArray[i] = points[i]
    }
    var n = ids.length
    var idArray = pool.mallocInt32(n)
    for(var i=0; i<n; ++i) {
      idArray[i] = ids[i]
    }
    var d = (nd/n)|0
    return new KDTree(
      ndarray(pointArray, [n,d]),
      idArray,
      n,
      d)
  } else {
    return new KDTree(null, null, 0, data.d)
  }
}