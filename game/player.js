function Player(name, color, location, isMrX) {
    let name = name;
    let color = color;
    let isMrX = isMrX;
    let location = location;

    let tickets = isMrX ? {
        taxi: 4,
        bus: 3,
        underground: 3,
        black: 5
    } : {
        taxi: 10,
        bus: 8,
        underground: 4
    };

    // getters
    this.getName = () => name;
    this.getColor = () => color;
    this.isMrX = () => isMrX;
    this.getLocation = () => location;
    this.getTickets = (type) => {}

    //setters
    this.setLocation = (loc) => location = 1 <= loc && loc <= 200 ? loc : location;
    this.use = (type) => {
        switch (type) {
            case 'bus':

        }
    }

}

module.exports = Player;