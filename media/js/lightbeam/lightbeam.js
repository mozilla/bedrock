var width = 1000, height = 1000;
var force, vizcanvas, vis;

var nodemap = {};
var nodes = [];
var edgemap = {};
var edges = [];
var aggregate;

var requestAnimationFrame =
    window.requestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.webkitRequestAnimationFrame;

function loadData(data){
    vis = d3.select('.vizcanvas');

    console.log(data);
    console.log('data arriving');
    nodemap = data;
    var node, edgename, edge;
    console.log('All data: %o', Object.keys(data));
    connections = Object.keys(data).map(function(key){
        node = data[key];
        node.lastAccess = new Date(node.lastAccess);
        node.firstAccess = new Date(node.firstAccess);
        if (node.linkedFrom){
            node.linkedFrom.forEach(function(name){
                var source = nodemap[name];
                if (!source){
                    nodemap[name] = source = {
                        name: name,
                        notVisited: true,
                        notSecure: true,
                        cookie: true
                    };
                }
                edgename = name + '->' + node.name;
                if (!edgemap[edgename]){
                    edge = {source: source, target: node, name: edgename};
                    edgemap[edgename] = edge;
                    edges.push(edge);
                }
            });
        }
        if (node.linkedTo){
            node.linkedTo.forEach(function(name){
                var target = nodemap[name];
                if (!target){
                    nodemap[name] = target = {
                        name: name,
                        notVisited: true,
                        notSecure: true,
                        cookie: true
                    };
                }
                edgename = node.name + '->' + name;
                if (!edgemap[edgename]){
                    edge = {source: node, target: target, name: edgename};
                    edgemap[edgename] = edge;
                    edges.push(edge);
                }
            });
        }
        return nodes.push(node);
    });
    aggregate = {
        allnodes: nodes,
        nodemap: nodemap,
        edges: edges,
        edgemap: edgemap
    };
    initGraph();
}


// UTILITIES FOR CREATING POLYGONS

function point(angle, size){
    return [Math.round(Math.cos(angle) * size), -Math.round(Math.sin(angle) * size)];
}

function polygon(points, size, debug){
    var increment = Math.PI * 2 / points;
    var angles = [], i;
    for (i = 0; i < points; i++){
        angles.push(i * increment + Math.PI/2); // add 90 degrees so first point is up
    }
    return angles.map(function(angle){ return point(angle, size); });
}

function polygonAsString(points, size){
    var poly = polygon(points, size);
    return poly.map(function(pair){return pair.join(',');}).join(' ');
}

// SET UP D3 HANDLERS

function initGraph(){
    // Initialize D3 layout and bind data
    force = d3.layout.force()
        .nodes(aggregate.allnodes)
        .links(aggregate.edges)
        .charge(-500)
        .size([width,height])
        .start();
    updateGraph();

    // update method
    force.on('tick', function(){
        vis.selectAll('.edge')
            .attr('x1', function(edge){ return edge.source.x; })
            .attr('y1', function(edge){ return edge.source.y; })
            .attr('x2', function(edge){ return edge.target.x; })
            .attr('y2', function(edge){ return edge.target.y; });
        vis.selectAll('.node').call(updateNodes);
    });

}

function updateGraph(){
        // Data binding for links
    var lines = vis.selectAll('.edge')
        .data(aggregate.edges, function(edge){ return edge.name; });

    lines.enter().insert('line', ':first-child')
        .classed('edge', true);

    lines.exit()
        .remove();

    var nodes = vis.selectAll('.node')
        .data(aggregate.allnodes, function(node){ return node.name; });

    nodes.call(force.drag);

    nodes.enter().append('g')
        .classed('visitedYes', function(node){ return node.visitedCount; })
        .classed('visitedNo', function(node){ return !node.visitedCount; })
        .call(addShape)
        .attr('data-name', function(node){ return node.name; })
        .classed('node', true);



    nodes.exit()
        .remove();
    requestAnimationFrame(updateGraph);
}


function addCircle(selection){
    selection
        .append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 12)
        .classed('site', true);
}

function addShape(selection){
    selection.filter('.visitedYes').call(addCircle);
    selection.filter('.visitedNo').call(addTriangle);
}

function addTriangle(selection){
    selection
        .append('polygon')
        .attr('points', polygonAsString(3, 20))
        .attr('data-name', function(node){ return node.name; });
}

function addSquare(selection){
    selection
        .append('rect')
        .attr('x', -9)
        .attr('y', -9)
        .attr('width', 18)
        .attr('height', 18);
}


function updateNodes(thenodes){
    thenodes
    .attr('transform', function(node){ return 'translate(' + node.x + ',' + node.y + ') scale(' + (1 + .03 * node.weight) + ')'; })
    .classed('secureYes', function(node){ return node.secureCount === node.howMany; })
    .classed('secureNo', function(node){ return node.secureCount !== node.howMany; })
    .classed('cookieYes', function(node){ return node.cookieCount })
    .classed('cookieNo', function(node){ return !node.cookieCount; })
    .attr('data-timestamp', function(node){ return node.lastAccess.toISOString(); });
    // change shape if needed
}
