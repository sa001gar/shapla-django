from django.shortcuts import render
from .models import Post, Category, TeamMember

# Create your views here.
def index(request):
    # Fetch Hero Post (Latest "Editorial" or just latest post)
    # Assuming 'editorial' slug for hero or just first post for now. 
    # Let's try to find an 'editorial' category, else fallback to latest.
    hero_post = Post.objects.filter(category__slug='editorial').first()
    if not hero_post:
        hero_post = Post.objects.first()

    # Helper to fetch posts by category slug
    def get_category_posts(slug):
        return Post.objects.filter(category__slug=slug)[:4]

    context = {
        'hero_post': hero_post,
        'politics_posts': get_category_posts('politics'),
        'sports_posts': get_category_posts('sports'),
        'feature_posts': get_category_posts('featured'),
        'opinion_posts': get_category_posts('opinion'),
        'international_posts': get_category_posts('international'),
        'entertainment_posts': get_category_posts('entertainment'),
        'education_posts': get_category_posts('education'),
        'team_members': TeamMember.objects.all()[:4],
    }
    
    return render(request, 'pages/index.html', context)
    
def authors(request):
    return render(request, 'pages/authors.html')

def category(request):
    return render(request, 'pages/categories.html')

def post(request):
    return render(request, 'pages/post-individual.html')

