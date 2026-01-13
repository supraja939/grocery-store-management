let products = [];

$(document).ready(function () {
    loadProducts();

    $("#addRowBtn").click(function () {
        addRow();
    });

    $("#saveOrderBtn").click(function () {
        saveOrder();
    });
});

function loadProducts() {
    $.get(API_URL + "/getProducts", function (data) {
        products = data;
        $("#orderTable").html("");
        addRow();
    });
}

function addRow() {
    let options = `<option value="">--Select--</option>`;
    products.forEach(p => {
        options += `<option value="${p.product_id}" data-price="${p.price}">${p.name}</option>`;
    });

    let row = `
        <tr>
            <td>
                <select class="form-select product" onchange="productChanged(this)">
                    ${options}
                </select>
            </td>
            <td><input type="text" class="form-control price" readonly></td>
            <td><input type="number" class="form-control qty" value="1" oninput="calculateRow(this)"></td>
            <td><input type="text" class="form-control total" readonly></td>
            <td><button class="btn btn-danger btn-sm" onclick="removeRow(this)">X</button></td>
        </tr>
    `;

    $("#orderTable").append(row);
}

function productChanged(select) {
    let price = $(select).find(":selected").data("price");
    let row = $(select).closest("tr");
    row.find(".price").val(price);
    calculateRow(row.find(".qty"));
}

function calculateRow(qtyInput) {
    let row = $(qtyInput).closest("tr");
    let price = row.find(".price").val();
    let qty = row.find(".qty").val();
    let total = price * qty;
    row.find(".total").val(total.toFixed(2));
    calculateGrandTotal();
}

function calculateGrandTotal() {
    let sum = 0;
    $(".total").each(function () {
        sum += Number($(this).val());
    });
    $("#grandTotal").val(sum.toFixed(2));
}

function removeRow(btn) {
    $(btn).closest("tr").remove();
    calculateGrandTotal();
}

function saveOrder() {
    let order = {
        customer_name: $("#customerName").val(),
        total: $("#grandTotal").val(),
        items: []
    };

    $("#orderTable tr").each(function () {
        let productId = $(this).find(".product").val();
        let qty = $(this).find(".qty").val();
        let total = $(this).find(".total").val();

        if (productId) {
            order.items.push({
                product_id: productId,
                quantity: qty,
                total_price: total
            });
        }
    });

    $.ajax({
        url: API_URL + "/insertOrder",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(order),
        success: function () {
            alert("Order Saved Successfully");
            window.location.href = "index.html";
        }
    });
}
