var cols = 30;
var rows = 30;
var grid = new Array(cols);
var w,h;
var path;
var openSet = [];
var closedSet = [];
var start;
var end;


function removeFromArray(arr,ele){

	for (var i = arr.length-1; i >= 0; i--) {
		if(arr[i] == ele){
			arr.splice(i,1);
		}
	}

}

function heuristic(a, b){
	var d = dist(a.i, a.j, b.i, b.j);
	//var d = abs(a.i-b.i) + abs(a.j-b.j);
	return d;
}

function Spot(i,j){

	this.i = i;
	this.j = j;
	this.f = 0;
	this.g = 0;
	this.h = 0;
	this.neighbours = [];
	this.previous = undefined;
	this.wall = false;

	if (random(1) < 0.4)
		this.wall = true;

	this.show = function(col) {
		fill(col)
		if (this.wall)
			fill(0);

		noStroke();
		rect(this.i*w, this.j*h, w, h);
	}

	this.addNeighbours = function(grid){

		var i= this.i;
		var j= this.j;
		if(j < rows-1)
			this.neighbours.push(grid[i][j+1]);
		if(j > 0)
			this.neighbours.push(grid[i][j-1]);
		if(i > 0)
			this.neighbours.push(grid[i-1][j]);
		if(i < cols-1)
			this.neighbours.push(grid[i+1][j]);
		if(i > 0 && j > 0)
			this.neighbours.push(grid[i-1][j-1]);
		if(i < cols-1 && j > 0)
			this.neighbours.push(grid[i+1][j-1]);
		if(i > 0 && j < rows-1)
			this.neighbours.push(grid[i-1][j+1]);
		if(i < cols-1 && j < rows-1)
			this.neighbours.push(grid[i+1][j+1]);
	}
}

function setup()
{
	createCanvas(400,400);
	console.log('A*');

	w = width/cols;
	h = height/rows;

	for (var i = 0; i < cols; i++){
		grid[i] = new Array(rows);
	}

	for(var i = 0; i < cols; i++){
		for(var j = 0;j < rows;j++){
			grid[i][j] = new Spot(i,j);
		}
	}

	for(var i = 0; i < cols; i++){
		for(var j = 0; j < rows; j++){
			grid[i][j].addNeighbours(grid);
		}
	}

	start = grid[0][0];
	end = grid[cols-1][rows-1];
	start.wall = false;
	end.wall = false;
	openSet.push(start);


	console.log(grid);
}




function draw(){

	if (openSet.length > 0){
		
		var winner = 0;
		for(var i = 0; i < openSet.length; i++){
			if(openSet[i].f < openSet[winner].f)
				winner = i;
		}

		var current = openSet[winner];

		if(current == end) {
			// Find the end
			noLoop();
			console.log("Done");
		}

		removeFromArray(openSet,current);
		closedSet.push(current);

		var neighbours = current.neighbours;
		for (var i = 0; i < neighbours.length; i++){
			var neighbour = neighbours[i];

			if (!closedSet.includes(neighbour) && !neighbour.wall){
				var tempG = current.g + 1;

				var newPath = false
				if (openSet.includes(neighbour) ){
					if (tempG < neighbour.g){
						newPath = true;
						neighbour.g = tempG;
					}
				} else {
					neighbour.g = tempG;
					newPath = true;
					openSet.push(neighbour);
				}

				if (newPath){
					neighbour.h = heuristic(neighbour, end);
					neighbour.f = neighbour.g + neighbour.h
					neighbour.previous = current;
				}
			}

		}

	} else {
		// no solution
		console.log("No solution");
		noLoop();
		return;
	}


	background(0);


	for(var i = 0; i < cols; i++){
		for(var j = 0; j < rows; j++){
			grid[i][j].show(color(255));
		}
	}

	for(var i = 0; i < closedSet.length; i++){
		closedSet[i].show(color(255,0,0));
	}

	for(var i = 0; i < openSet.length; i++){
		openSet[i].show(color(0,255,0));
	}

	
	path = [];
	var temp = current;
	path.push(temp);
	while (temp.previous){
		path.push(temp.previous)
		temp = temp.previous;
	}
	for( var i = 0;i < path.length; i++)
		path[i].show(color(0,0,255));
	
	noFill();
	stroke(255);
	beginShape();
	for ( var i = 0; i < path.length; i++)
		vertex(path[i].i*w+w/2, path[i].j*h+h/2);
	endShape();
	
}

