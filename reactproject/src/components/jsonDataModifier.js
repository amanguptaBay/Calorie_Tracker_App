export function getModificationHandler(jsonObject, key, callback, letCallbackInsertToDict = false){
    /*
        Basically starting with a json Obect and a key we create a DUI function that will shallow clone the object and modify it, then call a callback.
        Delete: Delete the key from the object
        Update (default): Update the key in the object with the jsonPayload
        Insert: Insert the jsonPayload at the key in the object (if letCallbackInsertToDict is true, then the callerKey value is inserted into the dict, else the existing key is updated)
    */
    return (action, jsonPayload, callerKey = null) => {
        let newObject = Array.isArray(jsonObject) ? [...jsonObject] : {...jsonObject};
        switch(action){
            case("Delete"):
                if(Array.isArray(jsonObject)){
                    console.log("Deleting from array")
                    newObject.splice(key, 1);
                }
                else{
                    console.log("Deleting from dict")
                    delete newObject[key];
                }
                break;
            case("Insert"):
                newObject = Array.isArray(jsonObject) ? [...jsonObject.slice(0,key),jsonPayload,...jsonObject.slice(key,)] : {...jsonObject, [letCallbackInsertToDict ? callerKey : key]: jsonPayload};
                break;
            //Default behavior is update
            default:
                newObject[key] = jsonPayload || newObject[key];
                break;
        }
    callback(newObject);
    }
}
