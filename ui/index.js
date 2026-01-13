$(document).ready(function () {
    $.get(API_URL + "/getOrders", function (data) {
        let table = "";
        let total = 0;

        data.forEach(order => {
            table += `
                <tr>
                    <td>${order.datetime}</td>
                    <td>${order.order_id}</td>
                    <td>${order.customer_name}</td>
                    <td>${order.total.toFixed(2)} Rs</td>
                </tr>
            `;
            total += order.total;
        });

        $("table tbody").html(table);
        $("table tfoot").html(`
            <tr>
                <td colspan="3" class="text-end"><b>Total</b></td>
                <td><b>${total.toFixed(2)} Rs</b></td>
            </tr>
        `);
    });
});
