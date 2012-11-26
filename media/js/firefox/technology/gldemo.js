/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var per_fragment_lighting_fs = [
"  #ifdef GL_ES",
"  precision highp float;",
"  #endif",
"  varying vec2 vTextureCoord;",
"  varying vec4 vTransformedNormal;",
"  varying vec4 vPosition;",
"  uniform float uMaterialShininess;",
"  uniform bool uShowSpecularHighlights;",
"  uniform bool uUseLighting;",
"  uniform bool uUseTextures;",
"  uniform vec3 uAmbientColor;",
"  uniform vec3 uPointLightingLocation;",
"  uniform vec3 uPointLightingSpecularColor;",
"  uniform vec3 uPointLightingDiffuseColor;",
"  uniform sampler2D uSampler;",
"  void main(void) {",
"    vec3 lightWeighting;",
"    if (!uUseLighting) {",
"      lightWeighting = vec3(1.0, 1.0, 1.0);",
"    } else {",
"      vec3 lightDirection = normalize(uPointLightingLocation - vPosition.xyz);",
"      vec3 normal = normalize(vTransformedNormal.xyz);",
"      float specularLightWeighting = 0.0;",
"      if (uShowSpecularHighlights) {",
"        vec3 eyeDirection = normalize(-vPosition.xyz);",
"        vec3 reflectionDirection = reflect(-lightDirection, normal);",
"        specularLightWeighting = pow(max(dot(reflectionDirection, eyeDirection), 0.0), uMaterialShininess);",
"      }",
"      float diffuseLightWeighting = max(dot(normal, lightDirection), 0.0);",
"      lightWeighting = uAmbientColor",
"        + uPointLightingSpecularColor * specularLightWeighting",
"        + uPointLightingDiffuseColor * diffuseLightWeighting;",
"    }",
"    vec4 fragmentColor;",
"    if (uUseTextures) {",
"      fragmentColor = texture2D(uSampler, vec2(vTextureCoord.s, vTextureCoord.t));",
"    } else {",
"      fragmentColor = vec4(1.0, 1.0, 1.0, 1.0);",
"    }",
"    gl_FragColor = vec4(fragmentColor.rgb * lightWeighting, fragmentColor.a);",
"  }"
].join("\n");

var per_fragment_lighting_vs = [
"  attribute vec3 aVertexPosition;",
"  attribute vec3 aVertexNormal;",
"  attribute vec2 aTextureCoord;",
"  uniform mat4 uMVMatrix;",
"  uniform mat4 uPMatrix;",
"  uniform mat4 uNMatrix;",
"  varying vec2 vTextureCoord;",
"  varying vec4 vTransformedNormal;",
"  varying vec4 vPosition;",
"  void main(void) {",
"    vPosition = uMVMatrix * vec4(aVertexPosition, 1.0);",
"    gl_Position = uPMatrix * vPosition;",
"    vTextureCoord = aTextureCoord;",
"    vTransformedNormal = uNMatrix * vec4(aVertexNormal, 1.0);",
"  }",
].join("\n");




var gl;

var nogl;

function initGL(canvas) {
    try {
        gl = canvas.getContext("experimental-webgl");
        gl.viewportWidth = canvas.width;
        gl.viewportHeight = canvas.height;
        nogl = false;
    } catch(e) {}
    if (!gl) {
        nogl = true;
        document.body.classList.add("nogl");
    }
}


function getShader(gl, str, isFragment) {
    var shader;
    if (isFragment) {
        shader = gl.createShader(gl.FRAGMENT_SHADER);
    } else {
        shader = gl.createShader(gl.VERTEX_SHADER);
    }

    gl.shaderSource(shader, str);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert(gl.getShaderInfoLog(shader));
        return null;
    }

    return shader;
}


var shaderProgram;
function initShaders() {
    var fragmentShader = getShader(gl, per_fragment_lighting_fs, true);
    var vertexShader = getShader(gl, per_fragment_lighting_vs, false);

    shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        alert("Could not initialise shaders");
    }

    gl.useProgram(shaderProgram);

    shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
    gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

    shaderProgram.vertexNormalAttribute = gl.getAttribLocation(shaderProgram, "aVertexNormal");
    gl.enableVertexAttribArray(shaderProgram.vertexNormalAttribute);

    shaderProgram.textureCoordAttribute = gl.getAttribLocation(shaderProgram, "aTextureCoord");
    gl.enableVertexAttribArray(shaderProgram.textureCoordAttribute);

    shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
    shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
    shaderProgram.nMatrixUniform = gl.getUniformLocation(shaderProgram, "uNMatrix");
    shaderProgram.samplerUniform = gl.getUniformLocation(shaderProgram, "uSampler");
    shaderProgram.materialShininessUniform = gl.getUniformLocation(shaderProgram, "uMaterialShininess");
    shaderProgram.showSpecularHighlightsUniform = gl.getUniformLocation(shaderProgram, "uShowSpecularHighlights");
    shaderProgram.useTexturesUniform = gl.getUniformLocation(shaderProgram, "uUseTextures");
    shaderProgram.useLightingUniform = gl.getUniformLocation(shaderProgram, "uUseLighting");
    shaderProgram.ambientColorUniform = gl.getUniformLocation(shaderProgram, "uAmbientColor");
    shaderProgram.pointLightingLocationUniform = gl.getUniformLocation(shaderProgram, "uPointLightingLocation");
    shaderProgram.pointLightingSpecularColorUniform = gl.getUniformLocation(shaderProgram, "uPointLightingSpecularColor");
    shaderProgram.pointLightingDiffuseColorUniform = gl.getUniformLocation(shaderProgram, "uPointLightingDiffuseColor");
}


function handleLoadedTexture(texture) {
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texture.image);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    gl.generateMipmap(gl.TEXTURE_2D);

    gl.bindTexture(gl.TEXTURE_2D, null);
    tick();
}


var earthTexture;
var galvanizedTexture;
function initTextures() {
    earthTexture = gl.createTexture();
    earthTexture.image = new Image();
    earthTexture.image.onload = function() {
        handleLoadedTexture(earthTexture)
    }
//    earthTexture.image.src = "earth.jpg";

    galvanizedTexture = gl.createTexture();
    galvanizedTexture.image = new Image();
    galvanizedTexture.image.onload = function() {
        handleLoadedTexture(galvanizedTexture)
    }
    galvanizedTexture.image.src = "/media/img/firefox/technology/texture.jpg";
}


var mvMatrix;
var mvMatrixStack = [];

function mvPushMatrix(m) {
    if (m) {
        mvMatrixStack.push(m.dup());
        mvMatrix = m.dup();
    } else {
        mvMatrixStack.push(mvMatrix.dup());
    }
}

function mvPopMatrix() {
    if (mvMatrixStack.length == 0) {
        throw "Invalid popMatrix!";
    }
    mvMatrix = mvMatrixStack.pop();
    return mvMatrix;
}

function loadIdentity() {
    mvMatrix = Matrix.I(4);
}


function multMatrix(m) {
    mvMatrix = mvMatrix.x(m);
}


function mvTranslate(v) {
    var m = Matrix.Translation($V([v[0], v[1], v[2]])).ensure4x4();
    multMatrix(m);
}


function createRotationMatrix(angle, v) {
    var arad = angle * Math.PI / 180.0;
    return Matrix.Rotation(arad, $V([v[0], v[1], v[2]])).ensure4x4();
}


function mvRotate(angle, v) {
    multMatrix(createRotationMatrix(angle, v));
}


var pMatrix;
function perspective(fovy, aspect, znear, zfar) {
    pMatrix = makePerspective(fovy, aspect, znear, zfar);
}


function setMatrixUniforms() {
    gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, false, new Float32Array(pMatrix.flatten()));
    gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, new Float32Array(mvMatrix.flatten()));

    var normalMatrix = mvMatrix.inverse();
    normalMatrix = normalMatrix.transpose();
    gl.uniformMatrix4fv(shaderProgram.nMatrixUniform, false, new Float32Array(normalMatrix.flatten()));
}


var teapotVertexPositionBuffer;
var teapotVertexNormalBuffer;
var teapotVertexTextureCoordBuffer;
var teapotVertexIndexBuffer;
function handleLoadedTeapot(teapotData) {
    teapotVertexNormalBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, teapotVertexNormalBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(teapotData.vertexNormals), gl.STATIC_DRAW);
    teapotVertexNormalBuffer.itemSize = 3;
    teapotVertexNormalBuffer.numItems = teapotData.vertexNormals.length / 3;

    teapotVertexTextureCoordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, teapotVertexTextureCoordBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(teapotData.vertexTextureCoords), gl.STATIC_DRAW);
    teapotVertexTextureCoordBuffer.itemSize = 2;
    teapotVertexTextureCoordBuffer.numItems = teapotData.vertexTextureCoords.length / 2;

    teapotVertexPositionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, teapotVertexPositionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(teapotData.vertexPositions), gl.STATIC_DRAW);
    teapotVertexPositionBuffer.itemSize = 3;
    teapotVertexPositionBuffer.numItems = teapotData.vertexPositions.length / 3;

    teapotVertexIndexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, teapotVertexIndexBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(teapotData.indices), gl.STREAM_DRAW);
    teapotVertexIndexBuffer.itemSize = 1;
    teapotVertexIndexBuffer.numItems = teapotData.indices.length;
}


function loadTeapot() {
    var request = new XMLHttpRequest();
    request.open("GET", "/media/js/firefox/technology/Teapot.json");
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            handleLoadedTeapot(JSON.parse(request.responseText));
        }
    }
    request.send();
}


var teapotAngle = 180;

function drawScene() {
    gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    if (teapotVertexPositionBuffer == null || teapotVertexNormalBuffer == null || teapotVertexTextureCoordBuffer == null || teapotVertexIndexBuffer == null) {
        return;
    }

    perspective(50, gl.viewportWidth / gl.viewportHeight, 0.1, 100.0);

    var specularHighlights = true;
    gl.uniform1i(shaderProgram.showSpecularHighlightsUniform, specularHighlights);

    var lighting = true;
    gl.uniform1i(shaderProgram.useLightingUniform, lighting);
    if (lighting) {
        gl.uniform3f(shaderProgram.ambientColorUniform, 0.2, 0.2, 0.2);
        gl.uniform3f(shaderProgram.pointLightingLocationUniform, -10, 4, -20);
        gl.uniform3f(shaderProgram.pointLightingSpecularColorUniform, 0.8, 0.8, 0.8);
        gl.uniform3f(shaderProgram.pointLightingDiffuseColorUniform, 0.8, 0.8, 0.8);
    }

    var texture = "galvanized";
    gl.uniform1i(shaderProgram.useTexturesUniform, texture != "none");

    loadIdentity();

    mvTranslate([0, 0, -30]);
    mvRotate(23.4, [1, 0, -1]);
    mvRotate(teapotAngle, [0, 1, 0]);
    gl.activeTexture(gl.TEXTURE0);
    if (texture == "earth") {
        gl.bindTexture(gl.TEXTURE_2D, earthTexture);
    } else if (texture == "galvanized") {
        gl.bindTexture(gl.TEXTURE_2D, galvanizedTexture);
    }
    gl.uniform1i(shaderProgram.samplerUniform, 0);

    gl.uniform1f(shaderProgram.materialShininessUniform, 12);

    gl.bindBuffer(gl.ARRAY_BUFFER, teapotVertexPositionBuffer);
    gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, teapotVertexPositionBuffer.itemSize, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, teapotVertexTextureCoordBuffer);
    gl.vertexAttribPointer(shaderProgram.textureCoordAttribute, teapotVertexTextureCoordBuffer.itemSize, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, teapotVertexNormalBuffer);
    gl.vertexAttribPointer(shaderProgram.vertexNormalAttribute, teapotVertexNormalBuffer.itemSize, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, teapotVertexIndexBuffer);
    setMatrixUniforms();
    gl.drawElements(gl.TRIANGLES, teapotVertexIndexBuffer.numItems, gl.UNSIGNED_SHORT, 0);
}



var teapotRotating = false;

function tick() {
    drawScene();
    teapotAngle += 1.5;
    if (teapotRotating)
        window.mozRequestAnimationFrame(tick);
}


function webGLStart() {
    var canvas = document.querySelector("#webgldemo canvas");
    initGL(canvas);
    initShaders();
    initTextures();
    loadTeapot();

    gl.clearColor(0.0, 0.0, 0.0, 0.0);

    gl.clearDepth(1.0);

    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    tick();
}

if (window.addEventListener) {
    window.addEventListener("load", webGLStart, true);
}

function startTeaPot() {
    if (nogl) return;
    teapotRotating = true; tick();
}
function stopTeaPot()  {
    if (nogl) return;
    teapotRotating = false;
}
