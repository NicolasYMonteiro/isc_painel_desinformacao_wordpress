<?php
if (!defined('ABSPATH')) {
    exit;
}

final class DSN_Pages
{
    public static function register(): void
    {
        add_action('init', [self::class, 'ensure_pages']);
    }

    public static function activate(): void
    {
        self::ensure_pages();
        flush_rewrite_rules();
    }

    public static function ensure_pages(): void
    {
        $pages = [
            'por-tema' => [
                'title' => 'Por Tema',
                'content' => '[dsn_dashboard page="tema"]',
            ],
            'por-plataforma' => [
                'title' => 'Por Plataforma',
                'content' => '[dsn_dashboard page="plataforma"]',
            ],
        ];

        foreach ($pages as $slug => $cfg) {
            $existing = get_page_by_path($slug);
            if ($existing) {
                continue;
            }
            wp_insert_post([
                'post_title' => $cfg['title'],
                'post_name' => $slug,
                'post_status' => 'publish',
                'post_type' => 'page',
                'post_content' => $cfg['content'],
            ]);
        }
    }
}
