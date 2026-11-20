document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("table").forEach((table) => {
        if (!table.querySelector("thead")) {
            return;
        }

        new DataTable(table, {
            paging: true,
            pagingType: "simple",
            searching: true,
            pageLength: 10,
            lengthChange: false,

            ordering: {
                indicators: false,
                handler: false,
            },

            columnControl: ["orderAsc", "orderDesc"],
        });
    });
});