<?php
/**
 * Plugin Name: DSN Dashboard
 * Description: Painel DSN-DASH — carrossel Por Tema / Por Plataforma com embeds Kibana e Shiny.
 * Version: 0.1.0
 * Author: DSN-DASH
 * Text Domain: dsn-dashboard
 */

if (!defined('ABSPATH')) {
    exit;
}

define('DSN_DASH_VERSION', '0.1.0');
define('DSN_DASH_PATH', plugin_dir_path(__FILE__));
define('DSN_DASH_URL', plugin_dir_url(__FILE__));

require_once DSN_DASH_PATH . 'includes/class-dsn-dashboard.php';
require_once DSN_DASH_PATH . 'includes/class-dsn-shortcode.php';
require_once DSN_DASH_PATH . 'includes/class-dsn-pages.php';

add_action('plugins_loaded', static function () {
    DSN_Dashboard::instance()->init();
});

register_activation_hook(__FILE__, ['DSN_Pages', 'activate']);
