<?php
if (!defined('ABSPATH')) {
    exit;
}

final class DSN_Dashboard
{
    private static ?self $instance = null;

    public static function instance(): self
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    public function init(): void
    {
        DSN_Shortcode::register();
        DSN_Pages::register();
        add_action('wp_enqueue_scripts', [$this, 'assets']);
        add_filter('body_class', [$this, 'body_class']);
    }

    public function assets(): void
    {
        if (!$this->is_dashboard_page()) {
            return;
        }

        wp_enqueue_style(
            'swiper',
            'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css',
            [],
            '11'
        );
        wp_enqueue_style(
            'dsn-dashboard',
            DSN_DASH_URL . 'assets/css/dsn-dashboard.css',
            ['swiper'],
            DSN_DASH_VERSION
        );

        wp_enqueue_script(
            'swiper',
            'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js',
            [],
            '11',
            true
        );
        wp_enqueue_script(
            'dsn-dashboard',
            DSN_DASH_URL . 'assets/js/dsn-dashboard.js',
            ['swiper'],
            DSN_DASH_VERSION,
            true
        );

        wp_localize_script('dsn-dashboard', 'dsnDash', [
            'kibanaUrl' => getenv('DSN_KIBANA_URL') ?: 'http://localhost:5601',
            'shinyUrl' => getenv('DSN_SHINY_URL') ?: 'http://localhost:3838',
            'transitionMs' => 280,
        ]);
    }

    public function body_class(array $classes): array
    {
        if ($this->is_dashboard_page()) {
            $classes[] = 'dsn-no-scroll';
        }
        return $classes;
    }

    private function is_dashboard_page(): bool
    {
        if (!is_singular()) {
            return false;
        }
        $post = get_post();
        return $post && has_shortcode($post->post_content, 'dsn_dashboard');
    }
}
