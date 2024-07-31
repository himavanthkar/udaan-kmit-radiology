function _initInterface() {
	initModeButtons();
	initToolButtons();
}

_initCornerstone();
const element = document.getElementById("dicomImage");
_initInterface();

var ptsLt = [];

cornerstoneTools.init({
	showSVGCursors: true,
});

cornerstoneTools.toolStyle.setToolWidth(4);

// // Set color for inactive tools
cornerstoneTools.toolColors.setToolColor("rgb(255, 255, 0)");

// Set color for active tools
cornerstoneTools.toolColors.setActiveColor("#eb2f06");
cornerstone.enable(element);

// var toolName = document.getElementById("selectingTool").value;
// document
// 	.getElementById("selectingTool")
// 	.addEventListener("click", function (e) {
// 		console.log("Clicked");
// 		// console.log(document.getElementById("selectingTool").value);
// 		toolName = document.getElementById("selectingTool").value;
// 		const apiTool = cornerstoneTools[`${toolName}Tool`];
// 		cornerstoneTools.addTool(apiTool);
// 		cornerstoneTools.setToolActive(toolName, {
// 			mouseButtonMask: 1,
// 		});
// 	});

// FreehandRoi, RectangleRoi
let currentImageIndex = 0;
var imageIds = [];
var dummy = [];

const stack = {
	currentImageIdIndex: 0,
	imageIds: imageIds,
};

function handleFileSelect() {
	// updateTheImage(0);
	cornerstone.loadImage(imageIds[0]).then(function (image) {
		// Display the first image
		cornerstone.displayImage(element, image);

		// Add the stack tool state to the enabled element
		cornerstoneTools.addStackStateManager(element, ["stack"]);
		cornerstoneTools.addToolState(element, "stack", stack);
	});
}

// ! Change dimensions for downloading image
function doResize(width, height, el) {
	el.style.width = width + "px";
	el.style.height = height + "px";
	cornerstone.resize(el);
}

document.getElementById("imageButton1").addEventListener("click", function () {
	if (currentImageIndex == imageIds.length - 1) {
		alert("This is last image please scroll -");
		currentImageIndex = imageIds.length - 2;
	} else {
		updateTheImage(currentImageIndex + 1);
	}
});

document.getElementById("imageButton2").addEventListener("click", function () {
	if (currentImageIndex == 0) {
		alert("This is last image please scroll +");
		currentImageIndex = 0;
	} else {
		updateTheImage(currentImageIndex - 1);
	}
});

// show image #1 initially
// var toWidth;
// var toHeight;
function updateTheImage(imageIndex) {
	currentImageIndex = imageIndex;
	// console.log(imageIds[currentImageIndex]);
	cornerstone.loadImage(imageIds[currentImageIndex]).then(function (image) {
		cornerstone.displayImage(element, image);
		// console.log(image.width);
		// console.log(image.height);
		// toWidth
	});
}

var allAnnotations;

function showData() {
	// let image = cornerstone.getImage(element);

	// image.width = 624;
	// image.height = 624;

	// cornerstone.resize(element, true);

	// let image = cornerstone.getImage(element);

	// element.style.width = "624px";
	// element.style.height = "624px";

	// image.rowPixelSpacing = parseInt(image.rowPixelSpacing, 10);
	// image.columnPixelSpacing = parseInt(
	//     image.columnPixelSpacing,
	//     10
	// );

	// cornerstone.resize(element, true);

	// console.log(cornerstone.getImage(element));
	// var toolState = cornerstoneTools.globalImageIdSpecificToolStateManager.saveToolState();
	// console.log(toolState[currimage.imageId]);
	// allAnnotations = toolState[currimage.imageId];
	// console.log(allAnnotations);
	// console.log(allAnnotations.FreehandRoi !== undefined);
	// console.log(toolName);
	//doResize(624, 624, element);
	var toolData = cornerstoneTools.getToolState(element, toolName);
	// console.log(toolData);
	for (var i = 0; i < toolData.data.length; i++) {
		ptsLt.push(toolData.data[i].handles.points);
	}
	console.log("Saved !!");
	// if (ptsLt != undefined) {
	//     console.log(ptsLt);
	// }
}

function saveImage() {
	let getimage = cornerstone.getImage(element);

	// doResize(624, 624, element);

	// setTimeout(function () {
	//     let naturalWidth = getimage.width;
	//     let naturalHeight = getimage.height;
	//     console.log(naturalWidth, naturalHeight);

	//     // let canvas = document.getElementById("canvas");
	//     var dummy = document.createElement("canvas");
	//     var oCanvas = document.createElement("canvas"); // making a dummy canvas to put image
	//     oCanvas.width = 624; // use the original size
	//     oCanvas.height = 624;
	//     // canvas.width = naturalWidth; // use the original size
	//     // canvas.height = naturalHeight;
	//     let context = oCanvas.getContext("2d");
	//     context.drawImage(dummy, 0, 0, 624, 624);

	//     ptsLt.forEach((item) => {
	//         //console.log(item);
	//         context.strokeStyle = "rgb(255,0,0)";
	//         context.fillStyle = "#FFFFFF"; // Filling rectangle color
	//         context.lineWidth = 2;
	//         context.globalCompositeOperation = "source-over";
	//         context.moveTo(item[0].x, item[0].y);
	//         for (var j = 1; j < item.length; j++) {
	//             context.lineTo(item[j].x, item[j].y);
	//         }
	//         context.fill();
	//     });

	//     let base64 = oCanvas.toDataURL("image/jpeg", 1.0);
	//     console.log(base64);
	//     if (base64.length > 12) {
	//         base64 = base64.replace(/^data:image\/\w+;base64,/, "");
	//         base64 = atob(base64);
	//         let count = base64.length;
	//         console.log(count);
	//         let u8arr = new Uint8Array(count);
	//         while (count--) {
	//             u8arr[count] = base64.charCodeAt(count);
	//         }
	//         let file = new File([u8arr], { type: "jpeg" });
	//         if (navigator.msSaveBlob) {
	//             // IE 10+
	//             navigator.msSaveBlob(file, "mask.jpg");
	//         } else {
	//             var link = document.createElement("a");
	//             if (link.download !== undefined) {
	//                 // feature detection
	//                 // Browsers that support HTML5 download attribute
	//                 var url = URL.createObjectURL(file);
	//                 link.setAttribute("href", url);
	//                 link.setAttribute("download", "mask.jpg");
	//                 link.style.visibility = "hidden";
	//                 document.body.appendChild(link);
	//                 link.click();
	//                 document.body.removeChild(link);
	//             }
	//         }
	//     }
	//     doResize(1438, 780, element);
	// }, 1000);

	let naturalWidth = getimage.width;
	let naturalHeight = getimage.height;
	console.log(naturalWidth, naturalHeight);

	// let canvas = document.getElementById("canvas");
	var dummy = document.createElement("canvas");
	var oCanvas = document.createElement("canvas"); // making a dummy canvas to put image
	oCanvas.width = naturalWidth; // use the original size
	oCanvas.height = naturalHeight;
	// canvas.width = naturalWidth; // use the original size
	// canvas.height = naturalHeight;
	let context = oCanvas.getContext("2d");
	context.drawImage(dummy, 0, 0, naturalWidth, naturalHeight);

	ptsLt.forEach((item) => {
		//console.log(item);
		context.strokeStyle = "rgb(255,0,0)";
		context.fillStyle = "#FFFFFF"; // Filling rectangle color
		context.lineWidth = 2;
		context.globalCompositeOperation = "source-over";
		context.moveTo(item[0].x, item[0].y);
		for (var j = 1; j < item.length; j++) {
			context.lineTo(item[j].x, item[j].y);
		}
		context.fill();
	});

	let base64 = oCanvas.toDataURL("image/jpeg", 1.0);
	// console.log(base64);
	if (base64.length > 12) {
		base64 = base64.replace(/^data:image\/\w+;base64,/, "");
		base64 = atob(base64);
		let count = base64.length;
		console.log(count);
		let u8arr = new Uint8Array(count);
		while (count--) {
			u8arr[count] = base64.charCodeAt(count);
		}
		let file = new File([u8arr], { type: "jpeg" });
		if (navigator.msSaveBlob) {
			// IE 10+
			navigator.msSaveBlob(file, "mask.jpg");
		} else {
			var link = document.createElement("a");
			if (link.download !== undefined) {
				// feature detection
				// Browsers that support HTML5 download attribute
				var url = URL.createObjectURL(file);
				link.setAttribute("href", url);
				link.setAttribute("download", "mask.jpg");
				link.style.visibility = "hidden";
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			}
		}
	}
}

function saveImageAsPNG() {
	doResize(624, 624, element);
	// Getting the original image width and height
	setTimeout(function () {
		let naturalWidth = element.style.width;
		let naturalHeight = element.style.height;

		var canvas = element.querySelector("canvas"); // getting dicom image

		var oCanvas = document.createElement("canvas"); // making a dummy canvas to put image
		oCanvas.width = naturalWidth; // use the original size
		oCanvas.height = naturalHeight;
		console.log(naturalWidth, naturalHeight);
		let context = oCanvas.getContext("2d");
		context.drawImage(canvas, 0, 0, naturalWidth, naturalHeight);

		//console.log(canvas.toDataURL("image/png"));
		let base64 = canvas.toDataURL("image/png", 1.0);
		//console.log(base64);
		if (base64.length > 12) {
			base64 = base64.replace(/^data:image\/\w+;base64,/, "");
			base64 = atob(base64);
			let count = base64.length;
			console.log(count);
			let u8arr = new Uint8Array(count);
			while (count--) {
				u8arr[count] = base64.charCodeAt(count);
			}
			let file = new File([u8arr], { type: "png" });
			if (navigator.msSaveBlob) {
				// IE 10+
				navigator.msSaveBlob(file, "output.png");
			} else {
				var link = document.createElement("a");
				if (link.download !== undefined) {
					// feature detection
					// Browsers that support HTML5 download attribute
					var url = URL.createObjectURL(file);
					link.setAttribute("href", url);
					link.setAttribute("download", "output.png");
					link.style.visibility = "hidden";
					document.body.appendChild(link);
					link.click();
					document.body.removeChild(link);
				}
			}
		}
		doResize(1438, 780, element);
	}, 1000);
}

// if (toolData !== undefined) {
//     // Put it into an object
//     console.log(toolData);
// }

let loaded = false;

function _initCornerstone() {
	// Externals
	cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
	cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
	cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
	cornerstoneTools.external.cornerstone = cornerstone;
	cornerstoneTools.external.Hammer = Hammer;
}

const convertMouseEventWhichToButtons = (which) => {
	switch (which) {
		// no button
		case 0:
			return 0;
		// left
		case 1:
			return 1;
		// middle
		case 2:
			return 4;
		// right
		case 3:
			return 2;
	}
	return 0;
};
var dcmList = [];

document.getElementById("fileImg").addEventListener("change", function (e) {
	// Add the file to the cornerstoneFileImageLoader and get unique
	// number for that file

	const files = document.getElementById("fileImg").files;
	console.log(files.length);

	// only Dicom files
	for (var i = 0, len = files.length; i < len; i++) {
		dcmList.push(files[i]);
	}

	function readAndPreview(file) {
		var reader = new FileReader();

		reader.addEventListener(
			"load",
			function () {
				const imageId =
					cornerstoneWADOImageLoader.wadouri.fileManager.add(file);
				// console.log(imageId);
				imageIds.push(imageId);
			},
			true
		);
		reader.readAsDataURL(file);
	}
	if (files) {
		// ! Sorts files by name

		const sortByName = (dcmList) => {
			return dcmList.sort((a, b) =>
				a["name"].localeCompare(
					b["name"],
					navigator.languages[0] || navigator.language,
					{ numeric: true, ignorePunctuation: true }
				)
			);
		};
		sortByName(dcmList);
		console.log(dcmList);
		// [].forEach.call(files, readAndPreview);
		for (var i = 0, len = dcmList.length; i < len; i++) {
			readAndPreview(dcmList[i]);
		}
	}
});
