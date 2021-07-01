// const AVAILABLE_COLORS = ['red', 'blue', 'purple', 'green', 'yellow', 'orange', 'X'];

function Player(con_id, player_name, player_location) {
    const id = con_id; // websocket connection ID
    const name = player_name;
    let color = player_color;
    let isMrX = player_isMrX;
    let location = player_location;

    let tickets = isMrX ? {
        taxi: 4,
        bus: 3,
        underground: 3,
        black: 5,
        times_two: 2
    } : {
        taxi: 10,
        bus: 8,
        underground: 4
    };

    // getters
    this.getID = () => id;
    this.getName = () => name;
    this.getColor = () => color;
    this.isMrX = () => isMrX;
    this.getLocation = () => location;
    this.getTickets = (type) => {
        switch (type) {
            case 'taxi':
                return tickets.taxi;
                break;
            case 'bus':
                return tickets.bus;
                break;
            case 'underground':
                return tickets.underground;
                break;
            case 'black':
                if (isMrX) return tickets.black;
                break;
        }
    }

    //setters
    this.setColor = c => {
        color = c;
    };
    this.setMrX = () => {
        isMrX = true;
        color = 'X';
    };
    this.unsetMrX = (c) => {
        isMrX = false;
        color = c;
    };
    this.setLocation = loc => location = 1 <= loc && loc <= 200 ? loc : location;
    this.discard = (type) => {
        switch (type) {
            case 'taxi':
                tickets.taxi--;
                break;
            case 'bus':
                tickets.bus--;
                break;
            case 'underground':
                tickets.underground--;
                break;
            case 'black':
                if (isMrX) tickets.black--;
                break;
            case 'times_two':
                if (isMrX) tickets.times_two--;
                break;
        }
    }

    this.gain = (type) => { // Gain tickets discarded by detectives
        if (isMrX) {
            switch (type) {
                case 'taxi':
                    tickets.taxi++;
                    break;
                case 'bus':
                    tickets.bus++;
                    break;
                case 'underground':
                    tickets.underground++;
                    break;
            }
        }
    }
}

module.exports = Player;