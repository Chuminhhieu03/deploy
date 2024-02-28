from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Expenses
import json
from django.contrib import messages
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.staticfiles.storage import staticfiles_storage
import io
import pandas as pd
from decimal import Decimal
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Q

font_path = ('static/fonts/DejaVuSans/DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVu', font_path))


def index(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        query = request.GET.get('q', '')
        user = request.user
        expenses = Expenses.objects.filter(
            Q(user=user) & (Q(description__icontains=query) | Q(amount__icontains=query) | Q(
                date__icontains=query) | Q(source__icontains=query))
        ).order_by('-date')
        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'expenses_table.htmL', {'page_obj': page_obj})


def chart(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'expenses_chart.html')


def get_chart_data(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        date = data.get('date')
        if date is None:
            return JsonResponse({'error': 'Missing date parameter'}, status=400)
        # Get the income data for the user and date provided by format mm/yyyy
        expenses = Expenses.objects.filter(user=user, date__month=date.split(
            '/')[0], date__year=date.split('/')[1])
        # Create a dictionary to store the expenses data
        expenses_data = [0, 0, 0, 0]
        # Loop through the expenses data and add the amount to the corresponding source
        for i in expenses:
            if i.source == '0':
                expenses_data[0] += i.amount
            elif i.source == '1':
                expenses_data[1] += i.amount
            elif i.source == '2':
                expenses_data[2] += i.amount
            elif i.source == '3':
                expenses_data[3] += i.amount
        # Return the expenses data as a JSON response
        if sum(expenses_data) == 0 or len(expenses) == 0:
            messages.warning(request, "Chưa có dữ liệu chi tiêu cho tháng này")
            # return fail message
            return JsonResponse({'error': 'Chưa có dữ liệu chi tiêu cho tháng này'}, status=400)
        return JsonResponse(expenses_data, safe=False)


def create_pdf(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.upgrade == False:
        messages.warning(request, "Bạn chưa nâng cấp tài khoản")
        return redirect('upgrade')
    user = request.user
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    expensess = Expenses.objects.filter(user=user)
    # convert amount to int and have a comma every 3 numbers
    for expenses in expensess:
        expenses.amount = '{:,}'.format(int(expenses.amount))
    SourceLable = ['Ăn uống', 'Quần áo', 'Du lịch và giải trí', 'Khác']
    p.setFont('DejaVu', 12)
    # i want to create a table for the expensess
    p.drawString(100, 750, f"Báo cáo Thu nhập cá nhân {user.username}")
    p.drawString(100, 730, "--------------------------------------------")
    p.drawString(100, 710, "Ngày")
    p.drawString(200, 710, "Loại")
    p.drawString(300, 710, "Chú thích")
    p.drawString(400, 710, "Tiền")
    y = 690
    for expenses in expensess:
        if y < 40:
            p.showPage()
            p.setFont('DejaVu', 12)
            p.drawString(100, 750, f"Báo cáo Thu nhập cá nhân {user.username}")
            p.drawString(
                100, 730, "--------------------------------------------")
            p.drawString(100, 710, "Ngày")
            p.drawString(200, 710, "Loại")
            p.drawString(300, 710, "Chú thích")
            p.drawString(400, 710, "Tiền")
            y = 690
        p.drawString(100, y, str(expenses.date))
        p.drawString(200, y, SourceLable[int(expenses.source)])
        p.drawString(300, y, expenses.description)
        p.drawString(400, y, str(expenses.amount) + " VNĐ")
        y -= 20

    # Close the PDF object cleanly, and end writing process.
    p.save()
    p.showPage()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    messages.success(request, 'Tạo báo cáo chi tiêu thành công')
    return FileResponse(io.BytesIO(pdf), as_attachment=True, filename='expensess.pdf')


def import_excel(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.upgrade == False:
        messages.warning(request, "Bạn chưa nâng cấp tài khoản")
        return redirect('upgrade')
    if request.method == 'POST':
        file = request.FILES['file']
        if not file.name.endswith('.xlsx') and not file.name.endswith('.xls'):
            messages.warning(
                request, 'Sai định dạng file, chỉ chấp nhận file excel có đuôi .xlsx hoặc .xls')
            return redirect('income')
        df = pd.read_excel(file)
        try:
            for i in range(len(df)):
                expenses = Expenses(user=request.user, amount=Decimal(float(
                    df['amount'][i])), date=df['date'][i], source=df['source'][i], description=df['description'][i])
                expenses.save()
        except:
            messages.warning(
                request, 'Kiểm tra lại định dạng file excel, có thể có lỗi trong quá trình import dữ liệu')
            return redirect('expenses')
        messages.success(request, 'Import thành công')
        return redirect('expenses')
    return redirect('expenses')


def add(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        return render(request, 'add_expenses.html')
    if request.method == 'POST':
        user = request.user
        amount = request.POST['amount']
        date = request.POST['date']
        source = request.POST['source']
        description = request.POST['description']
        expenses = Expenses(user=user, amount=amount, date=datetime.strptime(
            date, '%d/%m/%Y'), source=source, description=description)
        expenses.save()
        messages.success(request, 'Thêm chi tiêu thành công')
        return redirect('expenses')


def edit(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'GET':
        expenses = Expenses.objects.get(id=id)
        expenses.date = expenses.date.strftime('%d/%m/%Y')
        expenses.amount = int(expenses.amount)
        return render(request, 'edit_expenses.html', {'expenses': expenses})
    if request.method == 'POST':
        expenses = Expenses.objects.get(id=id)
        expenses.amount = request.POST['amount']
        date = request.POST['date']
        expenses.date = datetime.strptime(date, '%d/%m/%Y')
        expenses.source = request.POST['source']
        expenses.description = request.POST['description']
        expenses.save()
        messages.success(request, 'Chỉnh sửa chi tiêu thành công')
        return redirect('expenses')


def delete(request, id):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == 'POST':
        try:
            expenses = Expenses.objects.get(id=id)
            expenses.delete()
        except:
            messages.warning(request, 'Khoản chi tiêu không tồn tại')
            return redirect('expenses')
        messages.success(request, 'Xóa chi tiêu thành công')
        return redirect('expenses')
