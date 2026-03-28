# WordPress Theme Development Reference

## Template Hierarchy

```
style.css          → Theme stylesheet (required)
index.php          → Fallback template
header.php         → Common header
footer.php         → Common footer
sidebar.php        → Sidebar
functions.php      → Theme functions
```

### Main Templates
| Template | Purpose |
|----------|---------|
| `front-page.php` | Static front page |
| `home.php` | Blog posts index |
| `single.php` | Single post |
| `page.php` | Single page |
| `archive-{post-type}.php` | Custom post type archives |
| `search.php` | Search results |
| `404.php` | Not found page |

### Template Parts
```php
get_header();
get_footer();
get_sidebar();
get_template_part('content', 'page');
```

## Child Themes

### Required Files
**style.css (in child theme root)**
```css
/*
Theme Name:   My Child Theme
Template:     parent-theme-folder
Version:      1.0.0
Text Domain:  my-child-theme
*/
@import url('../parent-theme/style.css');
```

### functions.php
```php
<?php
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style(
        'child-theme-style',
        get_stylesheet_uri(),
        ['parent-theme-style'],
        wp_get_theme()->get('Version')
    );
});
```

## Full Site Editing (FSE)

### block-theme structure
```
theme/
├── theme.json          → Global settings & styles
├── templates/
│   ├── index.html
│   ├── front-page.html
│   ├── single.html
│   └── archive.html
├── parts/
│   ├── header.html
│   ├── footer.html
│   └── template-parts/
└── styles/
```

### theme.json example
```json
{
  "version": 2,
  "settings": {
    "appearanceTools": true,
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    }
  },
  "styles": {
    "color": {
      "background": "#ffffff",
      "text": "#1a1a1a"
    }
  }
}
```

## Theme Support

### functions.php add_theme_support
```php
add_theme_support('title-tag');
add_theme_support('post-thumbnails');
add_theme_support('custom-logo');
add_theme_support('html5', ['search-form', 'comment-form', 'comment-list']);
add_theme_support('automatic-feed-links');
add_theme_support('editor-styles');
add_theme_support('wp-block-styles');

add_image_size('featured', 1200, 675, true);
add_image_size('thumbnail', 300, 200, true);
```

## Customizer

### Add to Customizer
```php
function mytheme_customize_register($wp_customize) {
    // Section
    $wp_customize->add_section('mytheme_colors', [
        'title' => __('Colors', 'mytheme'),
        'priority' => 30
    ]);
    
    // Setting
    $wp_customize->add_setting('mytheme_primary_color', [
        'default' => '#0073aa',
        'sanitize_callback' => 'sanitize_hex_color'
    ]);
    
    // Control
    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'mytheme_primary_color', [
        'label' => __('Primary Color', 'mytheme'),
        'section' => 'mytheme_colors',
        'settings' => 'mytheme_primary_color'
    ]));
}
add_action('customize_register', 'mytheme_customize_register');
```

### Output in templates
```php
$primary = get_theme_mod('mytheme_primary_color', '#0073aa');
echo '<style>:root { --primary: ' . esc_attr($primary) . '; }</style>';
```

## Widgets

### Register Widget Area
```php
function mytheme_widgets_init() {
    register_sidebar([
        'name' => __('Main Sidebar', 'mytheme'),
        'id' => 'sidebar-1',
        'description' => __('Add widgets here.', 'mytheme'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget' => '</section>',
        'before_title' => '<h2 class="widget-title">',
        'after_title' => '</h2>'
    ]);
}
add_action('widgets_init', 'mytheme_widgets_init');
```

### Create Custom Widget
```php
class My_Widget extends WP_Widget {
    public function __construct() {
        parent::__construct(
            'my_widget',
            __('My Widget', 'mytheme'),
            ['description' => __('A custom widget', 'mytheme')]
        );
    }
    
    public function widget($args, $instance) {
        echo $args['before_widget'];
        if (!empty($instance['title'])) {
            echo $args['before_title'] . apply_filters('widget_title', $instance['title']) . $args['after_title'];
        }
        echo '<p>' . esc_html($instance['content']) . '</p>';
        echo $args['after_widget'];
    }
    
    public function form($instance) {
        $title = !empty($instance['title']) ? $instance['title'] : '';
        $content = !empty($instance['content']) ? $instance['content'] : '';
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Title:'); ?></label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo esc_attr($title); ?>">
        </p>
        <?php
    }
    
    public function update($new_instance, $old_instance) {
        $instance = [];
        $instance['title'] = (!empty($new_instance['title'])) ? strip_tags($new_instance['title']) : '';
        $instance['content'] = (!empty($new_instance['content'])) ? strip_tags($new_instance['content']) : '';
        return $instance;
    }
}
```

## Menu Locations

### Register in functions.php
```php
register_nav_menus([
    'primary' => __('Primary Menu', 'mytheme'),
    'footer' => __('Footer Menu', 'mytheme'),
    'mobile' => __('Mobile Menu', 'mytheme')
]);
```

### Display in template
```php
wp_nav_menu([
    'theme_location' => 'primary',
    'container' => 'nav',
    'container_class' => 'main-nav',
    'fallback_cb' => false,
    'items_wrap' => '<ul id="%1$s" class="%2$s">%3$s</ul>'
]);
```
