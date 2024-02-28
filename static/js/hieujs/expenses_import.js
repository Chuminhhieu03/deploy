document.getElementById('expenses_import_btn').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});
document.getElementById('fileInput').addEventListener('change', function(e) {
    var formExpenses = document.getElementById('expenses_import_form');
    formExpenses.submit();
});