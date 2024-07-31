// var viewer = OpenSeadragon({
//     id: "openseadragon1",
//     navigatorPosition: "TOP_RIGHT",
//     showNavigator: true,
//     prefixUrl: "{% static 'js/openseadragon/images/' %}",
//     tileSources: {
//         type: "image",
//         url: "../../media/2.png",
//         buildPyramid: false,
//     },
// });
// var anno = OpenSeadragon.Annotorious(viewer);

// function loadAnnotations(event) {
//     var annoFile = document.getElementById("loadingAnnoFile").files[0];
//     console.log(annoFile.name);
//     var userFile = document.getElementById("loadingAnnoFile");
//     userFile.src = URL.createObjectURL(userFile.files[0]);
//     var data = userFile.src;

//     // anno.loadAnnotations(
//     //     "../../media/annotationsFiles/annotationsFileNew.json"
//     // );
// }

var annotations = [];

anno.on("createAnnotation", function (data) {
    var dimensions = data.target.selector["value"];
    // console.log(data);
    // var annoName = data.name;
    // ! Only for Rectangle done
    // ! For polygon need to add
    var lt = dimensions.split(",");
    lt[0] = lt[0].slice(11, lt[0].length);
    annotations.push({
        AnnotationId: data.id,
        AnnotationName: data.body[0].value,
        imageName: data.target.source,
        x: lt[0],
        y: lt[1],
        width: lt[2],
        height: lt[3],
    });
    console.log(annotations);
});

// var today = new Date();
// var date =
//     today.getDate() + "-" + (today.getMonth() + 1) + "-" + today.getFullYear();

// var time =
//     today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
// var dateTime = date + " " + time;
// document.getElementById("currentDateTimeSave").innerHTML += dateTime;

function saveAnnotations() {
    console.log("Saved");
    document.getElementById("show").innerHTML += `<div
            class="alert alert-success alert-dismissible fade-out show"
            role="alert">
            <strong>Saved !!</strong>
            <br />
            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
            ></button>
        </div>`;
    console.log(anno.getAnnotations());
    // console.log(annotations[0].imageName);
}

function convertToCSV(objArray) {
    var array = typeof objArray != "object" ? JSON.parse(objArray) : objArray;
    var str = "";

    for (var i = 0; i < array.length; i++) {
        var line = "";
        for (var index in array[i]) {
            if (line != "") line += ",";

            line += array[i][index];
        }

        str += line + "\r\n";
    }

    return str;
}

function exportCSVFile(headers, items, fileTitle) {
    if (headers) {
        items.unshift(headers);
    }

    // Convert Object to JSON
    var jsonObject = JSON.stringify(items);

    var csv = this.convertToCSV(jsonObject);

    var exportedFilenmae = fileTitle + ".csv" || "export.csv";

    var blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    if (navigator.msSaveBlob) {
        // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) {
            // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = "hidden";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

function download_CSV() {
    if (annotations.length == 0 || annotations == null) {
        document.getElementById("show").innerHTML += `<div
            class="alert alert-danger alert-dismissible fade-out show"
            role="alert">
            <strong>No Annotations to download !!</strong>
            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
            ></button>
        </div>`;
    } else {
        var headers = {
            AnnotationId: "AnnotationId",
            AnnotationName: "AnnotationName",
            imageName: "imageName",
            x: "x",
            y: "y",
            width: "width",
            height: "height",
        };

        var fileTitle = "csv_Annotations";
        exportCSVFile(headers, annotations, fileTitle);
    }
}

function download_JSON() {
    if (annotations.length == 0 || annotations == null) {
        document.getElementById("show").innerHTML += `<div
        class="alert alert-danger alert-dismissible fade-out show"
        role="alert">
        <strong>No Annotations to download !!</strong>
        <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
        ></button>
    </div>`;
    } else {
        var newLt = anno.getAnnotations();
        var data = JSON.stringify(newLt);
        downloadJSONFile(data, "annotationsFile");
    }
}

function downloadJSONFile(data, givenName) {
    // data is the string type, that contains the contents of the file.
    // filename is the default file name, some browsers allow the user to change this during the save dialog.

    // Note that we use octet/stream as the mimetype
    // this is to prevent some browsers from displaying the
    // contents in another browser tab instead of downloading the file
    var filename = givenName + ".json" || "export.json";

    var blob = new Blob([data], { type: "octet/stream" });

    //IE 10+
    if (window.navigator.msSaveBlob) {
        window.navigator.msSaveBlob(blob, filename);
    } else {
        //Everything else
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.href = url;
        a.download = filename;

        setTimeout(() => {
            //setTimeout hack is required for older versions of Safari
            a.click();
            //Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }, 1);
    }
}

function download_AnnoPic() {
    if (annotations.length == 0 || annotations == null) {
        document.getElementById("show").innerHTML += `<div
        class="alert alert-danger alert-dismissible fade-out show"
        role="alert">
        <strong>No Annotations to download !!</strong>
        <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
        ></button>
    </div>`;
    } else {
        const image = new Image();
        image.src = annotations[0].imageName;
        let { naturalWidth, naturalHeight } = image;
        let canvas = document.createElement("canvas");
        canvas.width = image.naturalWidth; // use the original size
        canvas.height = image.naturalHeight;
        let context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, naturalWidth, naturalHeight);

        anno.getAnnotations().forEach((item) => {
            var dimensions = item.target.selector["value"];
            var lt = dimensions.split(",");
            lt[0] = lt[0].slice(11, lt[0].length);
            let x = lt[0];
            let y = lt[1];
            let width = lt[2];
            let height = lt[3];
            // context.shadowOffsetX = 3;
            // context.shadowOffsetY = 3;
            // context.shadowBlur = 3;
            // context.shadowColor = "rgba(255, 255, 255, 0.5)";
            context.strokeStyle = "rgb(255,0,0)";
            context.fillStyle = "#FFFFFF"; // Filling rectangle color
            //context.strokeStyle = "#FFFFFF";
            context.lineWidth = 2;
            // context.globalCompositeOperation = "destination-atop";
            // context.fillRect(x, y, width, height); // fillRect or strokeRect
            context.globalCompositeOperation = "source-over";
            context.strokeRect(x, y, width, height); // fillRect or strokeRect
        });

        let base64 = canvas.toDataURL("image/jpeg", 1.0);
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
                navigator.msSaveBlob(file, "output.jpg");
            } else {
                var link = document.createElement("a");
                if (link.download !== undefined) {
                    // feature detection
                    // Browsers that support HTML5 download attribute
                    var url = URL.createObjectURL(file);
                    link.setAttribute("href", url);
                    link.setAttribute("download", "output.jpg");
                    link.style.visibility = "hidden";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            }
        }
    }
}
