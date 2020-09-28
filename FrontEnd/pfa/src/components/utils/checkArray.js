export const checkArray = (array) => {
    // console.log(`size ->> ${array.length} ${array}`)
    if ((typeof array !== undefined && array.length > 0)) {
        return array
    } else {
        console.log(array);
        throw new Error("Array invalid or empty");
    }
};
