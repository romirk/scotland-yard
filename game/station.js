function Station(n) {
    const location = n;
    const neighbours = {
        taxi: [],
        bus: [],
        underground: [],
        special: []
    }

    this.getLocation = () => location;
    this.getAllNeighbours = () => neighbours;

    this.getNeighbours = type => {
        switch (type) {
            case 'taxi':
            case 0:
                return neighbours.taxi;
            case 'bus':
            case 1:
                return neighbours.bus;
            case 'underground':
            case 2:
                return neighbours.underground;
            case 'special':
            case 3:
                return neighbours.special;
        }
    }

    this.addNeighbour = (type, station) => {
        switch (type) {
            case 'taxi':
            case 0:
                neighbours.taxi.push(station);
                break;
            case 'bus':
            case 1:
                neighbours.bus.push(station);
                break;
            case 'underground':
            case 2:
                neighbours.underground.push(station);
                break;
            case 'special':
            case 3:
                neighbours.special.push(station);
                break;
            default:
                return false;
        }
        return true;
    }
}

module.exports = Station;