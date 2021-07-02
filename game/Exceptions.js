function Exception() {
    switch (arguments.length) {
        case 2:
            this.data = arguments[1];
        case 1:
            this.message = arguments[0];
        default:
            break;
    }
}

module.exports = Exception;