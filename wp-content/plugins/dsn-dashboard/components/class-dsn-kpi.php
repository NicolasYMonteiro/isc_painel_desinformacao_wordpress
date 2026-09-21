<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * KPIs nativos do mosaico (HTML — sem iframe).
 */
final class DSN_KPI
{
    /**
     * @param array<int, array{id:string,label:string,value:mixed,format:string,delta_pct:?float,period_label:string}> $kpis
     */
    public static function render_row(array $kpis): string
    {
        ob_start();
        echo '<div class="mosaic-cell mosaic-cell--kpis" data-mosaic-slot="kpis">';
        echo '<div class="dsn-kpi-row">';
        foreach ($kpis as $kpi) {
            echo self::render_card($kpi);
        }
        echo '</div></div>';
        return (string) ob_get_clean();
    }

    /**
     * @param array{id:string,label:string,value:mixed,format:string,delta_pct:?float,period_label:string} $kpi
     */
    public static function render_card(array $kpi): string
    {
        $value = self::format_value($kpi['value'], $kpi['format'] ?? 'int');
        $delta = $kpi['delta_pct'] ?? null;
        $delta_html = '';
        if ($delta !== null) {
            $dir = $delta >= 0 ? 'up' : 'down';
            $arrow = $delta >= 0 ? '↑' : '↓';
            $delta_html = sprintf(
                '<span class="dsn-kpi__delta dsn-kpi__delta--%s" aria-label="Variação %s">%s %s%%</span>',
                esc_attr($dir),
                esc_attr((string) $delta),
                $arrow,
                esc_html(number_format(abs((float) $delta), 1, ',', '.'))
            );
        }

        return sprintf(
            '<article class="dsn-kpi" data-kpi-id="%s">'
            . '<p class="dsn-kpi__label">%s</p>'
            . '<p class="dsn-kpi__value">%s</p>'
            . '%s'
            . '<p class="dsn-kpi__period">%s</p>'
            . '</article>',
            esc_attr($kpi['id']),
            esc_html($kpi['label']),
            esc_html($value),
            $delta_html,
            esc_html($kpi['period_label'] ?? '')
        );
    }

    private static function format_value(mixed $value, string $format): string
    {
        if ($format === 'text') {
            return (string) $value;
        }
        if ($format === 'pct') {
            return number_format((float) $value, 1, ',', '.') . '%';
        }
        return number_format((float) $value, 0, ',', '.');
    }

    /**
     * @return array{kpis: array<int, array>, slice?: array}|null
     */
    public static function load_json(string $relative_under_plugin): ?array
    {
        $path = DSN_DASH_PATH . ltrim($relative_under_plugin, '/\\');
        if (!is_readable($path)) {
            return null;
        }
        $raw = file_get_contents($path);
        if ($raw === false) {
            return null;
        }
        $data = json_decode($raw, true);
        return is_array($data) ? $data : null;
    }
}
