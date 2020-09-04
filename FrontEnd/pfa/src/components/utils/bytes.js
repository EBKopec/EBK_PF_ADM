export const base64ToBlob = (base64, mimetype, slicesize) => {
    // if (!decodeURIComponent(escape(window.atob(b64))) || !window.Uint8Array) {
    //     // The current browser doesn't have the atob function. Cannot continue
    //     return null;
    // }
    mimetype = mimetype || '';
    slicesize = slicesize || 1024;
    var bytechars = base64;
    var bytearrays = [];
    for (var offset = 0; offset < bytechars.length; offset += slicesize) {
        var slice = bytechars.slice(offset, offset + slicesize);
        var bytenums = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            bytenums[i] = slice.charCodeAt(i);
        }
        var bytearray = new Uint8Array(bytenums);
        bytearrays[bytearrays.length] = bytearray;
    }
    return new Blob(bytearrays, { type: mimetype });
};

export const downloadFile = (blob, filename) => {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display:none";
    var url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
};

export const str2bytes = (str) => {
    console.log(str.length)
    var bytes = new Uint8Array(str.length);
    for (var i=0; i<str.length; i++) {
       bytes[i] = str.charCodeAt(i);
     }
     return bytes;
 }

 export const checkArray = (array) => {
     
    if (typeof array !== undefined && Object.values(array).length > 0) {
        return array
    } else {
        console.log(array);
        throw new Error("Array invalid or empty");
    }
};