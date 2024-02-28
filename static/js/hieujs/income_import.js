document.getElementById('income_import_btn').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});
document.getElementById('fileInput').addEventListener('change', function(e) {
    var formIncome = document.getElementById('income_import_form');
    formIncome.submit();
});