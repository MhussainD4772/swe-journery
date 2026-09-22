enum Status {
    Active = "ACTIVE",
    Pending = "PENDING",
    Cancelled = "CANCELLED",
}

function describeStatus(status: Status) : string {
    switch (status) {
        case Status.Active:
            return "The status is active.";
        case Status.Pending:
            return "The status is pending.";
        case Status.Cancelled:
            return "The status is cancelled.";
        default:
            return "Unknown status.";
    }
}

console.log(Status.Pending);
