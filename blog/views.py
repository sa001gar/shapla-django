from django.shortcuts import render
from .models import Post, Category, TeamMember
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 15) # Cache for 15 minutes
def index(request):
    # Fetch Hero Post (Latest "Editorial" or just latest post)
    # Assuming 'editorial' slug for hero or just first post for now. 
    # Let's try to find an 'editorial' category, else fallback to latest.
    hero_post = Post.objects.filter(category__slug='editorial').select_related('author', 'category').first()
    if not hero_post:
        hero_post = Post.objects.select_related('author', 'category').first()

    # Helper to fetch posts by category slug
    def get_category_posts(slug):
        return Post.objects.filter(category__slug=slug).select_related('author', 'category')[:4]

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

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category).select_related('author', 'category')
    
    paginator = Paginator(posts_list, 6) # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'pages/categories.html', context)

def post(request, category_slug, post_slug):
    # Use select_related to fetch connected Author and Category in one go
    post = get_object_or_404(Post.objects.select_related('author', 'category'), slug=post_slug, category__slug=category_slug)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id).select_related('author', 'category')[:2]
    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'pages/post-individual.html', context)

def dashboard_callback(request, context):
    from .models import Post, Category, Author # Import needed within function to avoid circular imports
    context.update({
        "kpi": [
            {
                "title": "Total Posts",
                "metric": Post.objects.count(),
                "footer": "All time",
            },
            {
                 "title": "Categories",
                 "metric": Category.objects.count(),
            },
               {
                 "title": "Authors",
                 "metric": Author.objects.count(),
            },
        ],
    })
    return context
