<?php
if (!defined('ABSPATH')) {
    exit;
}

final class DSN_Shortcode
{
    public static function register(): void
    {
        add_shortcode('dsn_dashboard', [self::class, 'render']);
    }

    public static function render($atts = []): string
    {
        $atts = shortcode_atts(
            [
                'page' => 'tema',
                'slide' => '1',
                'height' => '70vh',
            ],
            $atts,
            'dsn_dashboard'
        );

        $page = in_array($atts['page'], ['tema', 'plataforma'], true) ? $atts['page'] : 'tema';
        $initial = max(1, min(4, (int) $atts['slide']));
        $height = esc_attr($atts['height']);

        $slides = self::slides_for($page);
        $kibana = esc_url(getenv('DSN_KIBANA_URL') ?: 'http://localhost:5601');
        $shiny = esc_url(getenv('DSN_SHINY_URL') ?: 'http://localhost:3838');

        ob_start();
        ?>
        <div class="dsn-dashboard" data-page="<?php echo esc_attr($page); ?>" data-initial-slide="<?php echo (int) $initial; ?>">
            <div class="dsn-shell-header">
                <nav class="dsn-nav" aria-label="Eixos do painel">
                    <a class="dsn-nav__link<?php echo $page === 'tema' ? ' is-active' : ''; ?>" href="<?php echo esc_url(home_url('/por-tema/')); ?>">Por Tema</a>
                    <a class="dsn-nav__link<?php echo $page === 'plataforma' ? ' is-active' : ''; ?>" href="<?php echo esc_url(home_url('/por-plataforma/')); ?>">Por Plataforma</a>
                </nav>
                <span class="dsn-badge-fake" role="status">Dados fictícios — demonstração</span>
            </div>

            <div class="swiper dsn-swiper" style="--dsn-embed-height: <?php echo $height; ?>">
                <div class="swiper-wrapper">
                    <?php foreach ($slides as $i => $slide) :
                        $idx = $i + 1;
                        $type = $slide['type'];
                        $src = $type === 'kibana'
                            ? $kibana . $slide['path']
                            : $shiny . $slide['path'];
                        $state = $slide['state'] ?? 'loading';
                        $title = esc_attr($slide['title']);
                        ?>
                        <div class="swiper-slide dsn-slide"
                             data-slide-index="<?php echo (int) $idx; ?>"
                             data-embed-type="<?php echo esc_attr($type); ?>"
                             data-state="<?php echo esc_attr($state); ?>">
                            <p class="dsn-slide-caption"><?php echo esc_html($slide['caption']); ?></p>
                            <p class="dsn-slide-indicator" aria-live="polite">
                                <span class="dsn-slide-pos"><?php echo (int) $idx; ?></span> / 4
                            </p>
                            <div class="dsn-embed-frame">
                                <?php if ($state === 'empty') : ?>
                                    <div class="dsn-state dsn-state--empty" role="status">Dado indisponível neste slide</div>
                                <?php else : ?>
                                    <div class="dsn-state dsn-state--loading" hidden>Carregando visualização…</div>
                                    <div class="dsn-state dsn-state--error" hidden>Visualização temporariamente indisponível</div>
                                    <iframe
                                        class="dsn-embed-iframe"
                                        title="<?php echo $title; ?>"
                                        src="<?php echo esc_url($src); ?>"
                                        loading="<?php echo $idx === $initial ? 'eager' : 'lazy'; ?>"
                                        referrerpolicy="no-referrer-when-downgrade"
                                    ></iframe>
                                <?php endif; ?>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
                <button type="button" class="swiper-button-prev dsn-ctrl" aria-label="Slide anterior"></button>
                <button type="button" class="swiper-button-next dsn-ctrl" aria-label="Próximo slide"></button>
                <div class="swiper-pagination dsn-pagination" aria-label="Posição do carrossel"></div>
            </div>
        </div>
        <?php
        return (string) ob_get_clean();
    }

    /**
     * @return array<int, array{type:string,path:string,caption:string,title:string,state?:string}>
     */
    private static function slides_for(string $page): array
    {
        if ($page === 'plataforma') {
            return [
                [
                    'type' => 'kibana',
                    'path' => '/app/dashboards#/view/dsn-by-platform?embed=true&_g=()',
                    'caption' => 'Volume de menções fictícias por plataforma (2021–2024).',
                    'title' => 'Kibana — menções por plataforma',
                ],
                [
                    'type' => 'kibana',
                    'path' => '/app/dashboards#/view/dsn-by-platform-year?embed=true&_g=()',
                    'caption' => 'Comparativo anual entre plataformas (agregação descritiva).',
                    'title' => 'Kibana — plataformas por ano',
                ],
                [
                    'type' => 'shiny',
                    'path' => '/dsn/',
                    'caption' => 'Engajamento agregado por plataforma (ggplot2 / Shiny).',
                    'title' => 'Shiny — engajamento por plataforma',
                ],
                [
                    'type' => 'shiny',
                    'path' => '/dsn/',
                    'caption' => 'Leitura complementar por canal — apenas contagens e somas.',
                    'title' => 'Shiny — visão complementar por plataforma',
                ],
            ];
        }

        return [
            [
                'type' => 'kibana',
                'path' => '/app/dashboards#/view/dsn-by-theme?embed=true&_g=()',
                'caption' => 'Distribuição de eventos fictícios por tema ao longo dos anos.',
                'title' => 'Kibana — eventos por tema',
            ],
            [
                'type' => 'kibana',
                'path' => '/app/dashboards#/view/dsn-theme-engagement?embed=true&_g=()',
                'caption' => 'Engajamento somado por tema (sem modelos preditivos).',
                'title' => 'Kibana — engajamento por tema',
            ],
            [
                'type' => 'shiny',
                'path' => '/dsn/',
                'caption' => 'Gráfico descritivo Shiny alinhado ao eixo tema.',
                'title' => 'Shiny — visão por tema',
            ],
            [
                'type' => 'shiny',
                'path' => '/dsn/',
                'caption' => 'Síntese visual complementar — dados de demonstração.',
                'title' => 'Shiny — síntese temática',
                // slide 4 pode simular empty via query ?dsn_empty=1 em testes
                'state' => isset($_GET['dsn_empty']) ? 'empty' : 'loading',
            ],
        ];
    }
}
