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
                return edges.taxi;
            case 'bus':
            case 1:
                return edges.bus;
            case 'underground':
            case 2:
                return edges.underground;
            case 'special':
            case 3:
                return edges.special;
        }
    }

    this.addNeighbour = (type, station) => {
        switch (type) {
            case 'taxi':
            case 0:
                edges.taxi.push(station);
                break;
            case 'bus':
            case 1:
                edges.bus.push(station);
                break;
            case 'underground':
            case 2:
                edges.underground.push(station);
                break;
            case 'special':
            case 3:
                edges.special.push(station);
                break;
            default:
                return false;
        }
        return true;
    }
}

module.exports = Station;