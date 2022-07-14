from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from.models import Todo, AppUser

# Create your views here.
#redirecting root '' to todos view
def redir(request):
    return redirect('todos:todos')

#todos view
def index(request):
    # checking to see if user is logged in
    if request.user.is_authenticated:
        #if they are, I am grabbing their event objects to display on their home screen and then
        # creating a data package with their full name and their objects
        full_name = f"{request.user.first_name} {request.user.last_name}"
        data = {'full_name': full_name, 'item_list': Todo.objects.filter(owner=request.user.id).values()}
        #rendering the home page with their data so they get a greeting in navbar and their events are
        #displayed on home screen
        return render(request, 'to-do-app/todos.html', data)
    else:
        #if not logged in I am rendering home page with no data
        return render(request, 'to-do-app/todos.html')

#new item view
def new(request):
    #if post then grabbing values
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        #creating a new item and saving it
        item = Todo(owner=request.user, title=title, description=description, due_date=due_date)
        item.save()
        
        return redirect('todos:see_item', id=item.id)
    #if request is a get request, just rendering the new page
    if request.method == 'GET':
        return render(request, 'to-do-app/new.html')

#view to see single item after creation
def see_item(request, id):
    #grabbing item by id
    item = Todo.objects.filter(id=id).values()[0]
    #puling out item detaials and setting to dict
    details = {
        'id': id,
        'title': item['title'],
        'description': item['description'],
        'created_date': item['created_date'],
        'due_date': item['due_date'],
    }
    #packaging into a dict to render
    data = { 'item_list': [details] }
    
    #rendering the home page but passing it a list of only one item
    return render(request, 'to-do-app/todos.html', data)

#edit item view
def edit(request, id):
    #if get, getting item by id then packaging to render on an edit page
    if request.method == 'GET':
        item = Todo.objects.get(id=id)
        details = {
            'id': id,
            'title': item.title,
            'description': item.description,
            'created_date': item.created_date,
            'due_date': item.due_date,
        }

        data = { 'item': details }
        #rendering edit page with data dict of item details
        return render(request, 'to-do-app/edit.html', data)

    #if post getting the item updated details
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']

        #grabbing the item by id then re-assigning the  values
        item = Todo.objects.get(id=id)
        item.title = title
        item.description = description
        item.due_date = due_date
        #saving the item
        item.save()
        #redirecting back to the homepage
        return redirect('todos:todos')

#view to delete the item
def delete(request, id):
    #getting item by id and then deleting it
    item = Todo.objects.get(id=id)
    item.delete()
    #redirecting to home page
    return redirect('todos:todos')

#view for sign up
def sign_up(request):
    #if post, pulling out user deatails and assigning the email to username for good measure
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            #creating new user
            AppUser.objects.create_user(first_name=first_name, last_name=last_name,  username=username, email=email, password=password)
            
        except Exception as e:
            print('oops!')
            print(str(e))
        #since the user just signed up successfully I am logging them in so they are logged in when
        # re-directed to home page    
        user = authenticate(email=email, password=password)
        login(request, user)
        #returning friendly message to be alerted to user
        return JsonResponse({'status': 'Account created successfully!'})
    
    #if get request just rendering the base signup page
    return render(request, 'to-do-app/sign_up.html') 

#login view
def log_in(request):
    #if post, grabbing values
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        #grabbing the user
        user = authenticate(email=email, password=password)
        
        #logging them in if they exist and are active user
        if user is not None:
            if user.is_active:
                try:
                    login(request, user)
                except Exception as e:
                    print('oops!')
                    print(str(e))
        #friendly messages depending on outcome to be displayed to user in an alert
                return JsonResponse({'status': 'Successfully logged in!'})
            else:
                return JsonResponse({'status': 'User not active!'})
        else:
            return JsonResponse({'status': 'No user!'})
    
    #if get request then rendering the login page
    return render(request, 'to-do-app/login.html') 


#signout view, pretty self explanatory
def sign_out(request):
    logout(request)
    return render(request, 'to-do-app/todos.html')
