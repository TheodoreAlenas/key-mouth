export default class Socket {
    constructor(getInput, setOutput) {
        this.getInput = getInput
        this.setOutput = setOutput

        setTimeout(function() {
            setOutput([{name: "bagasas", message: "stfu"}])
            console.log("modified")
        }, 1000)
    }
    close() {
        console.log("socket would close here")
    }
}
