<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Shells mosaico Padrões A / B / C / D (CSS Grid 12).
 * RNF-003: 1 dashboard Kibana multi-painel por slide (1 iframe).
 */
final class DSN_Mosaic
{
    private const KIBANA_G = "(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'2021-01-01T00:00:00.000Z',to:'2025-01-01T00:00:00.000Z'))";

    public static function render(array $spec, string $kibana_base, bool $eager): string
    {
        $pattern = $spec['pattern'] ?? 'A';
        $mod = match ($pattern) {
            'B' => 'dsn-mosaic--pattern-b',
            'C' => 'dsn-mosaic--pattern-c',
            'D' => 'dsn-mosaic--pattern-d',
            default => 'dsn-mosaic--pattern-a',
        };

        $chart = $spec['charts']['dashboard'] ?? null;
        if (!$chart) {
            return '<!-- mosaic: missing dashboard chart -->';
        }
        $src = $kibana_base . $chart['path'];

        ob_start();
        ?>
        <div class="dsn-mosaic <?php echo esc_attr($mod); ?>"
             data-mosaic-pattern="<?php echo esc_attr($pattern); ?>"
             data-slice-dimension="<?php echo esc_attr($spec['slice']['dimension']); ?>"
             data-slice-value="<?php echo esc_attr($spec['slice']['value']); ?>">
            <header class="mosaic-cell mosaic-cell--title">
                <h2 class="dsn-mosaic__title"><?php echo esc_html($spec['title']); ?></h2>
                <p class="dsn-mosaic__question"><?php echo esc_html($spec['question']); ?></p>
            </header>

            <?php echo DSN_KPI::render_row($spec['kpis']); ?>

            <div class="mosaic-cell mosaic-cell--charts" data-mosaic-slot="charts">
                <?php echo self::embed_wrapper($src, $chart['title'], $eager); ?>
            </div>
        </div>
        <?php
        return (string) ob_get_clean();
    }

    public static function embed_path(string $dashboard_id): string
    {
        return '/app/dashboards#/view/' . $dashboard_id
            . '?embed=true&_g=' . self::KIBANA_G
            . '&hide-filter-bar=true';
    }

    private static function embed_wrapper(string $src, string $title, bool $eager): string
    {
        $loading = $eager ? 'eager' : 'lazy';
        ob_start();
        ?>
        <div class="embed-wrapper dsn-embed-frame">
            <div class="dsn-state dsn-state--loading" hidden>Carregando visualização…</div>
            <div class="dsn-state dsn-state--error" hidden>Visualização temporariamente indisponível</div>
            <iframe
                class="dsn-embed-iframe"
                title="<?php echo esc_attr($title); ?>"
                src="<?php echo esc_attr($src); ?>"
                loading="<?php echo esc_attr($loading); ?>"
                referrerpolicy="no-referrer-when-downgrade"
                allow="fullscreen"
            ></iframe>
        </div>
        <?php
        return (string) ob_get_clean();
    }
}
