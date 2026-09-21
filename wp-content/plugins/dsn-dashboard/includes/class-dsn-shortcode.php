<?php
if (!defined('ABSPATH')) {
    exit;
}

final class DSN_Shortcode
{
    /** Janela temporal alinhada ao seed 2021–2024 (Rison Kibana). */
    private const KIBANA_G = "(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'2021-01-01T00:00:00.000Z',to:'2025-01-01T00:00:00.000Z'))";

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
        $kibana = rtrim((string) (getenv('DSN_KIBANA_URL') ?: 'http://localhost:5601'), '/');
        $shiny = rtrim((string) (getenv('DSN_SHINY_URL') ?: 'http://localhost:3838'), '/');

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
                        $eager = $idx === $initial;
                        $layout = $slide['layout'] ?? 'single';
                        ?>
                        <div class="swiper-slide dsn-slide<?php echo $layout === 'mosaic' ? ' dsn-slide--mosaic' : ''; ?>"
                             data-slide-index="<?php echo (int) $idx; ?>"
                             data-embed-type="<?php echo esc_attr($slide['type'] ?? 'kibana'); ?>"
                             data-layout="<?php echo esc_attr($layout); ?>"
                             data-state="<?php echo esc_attr($slide['state'] ?? 'loading'); ?>">
                            <?php if ($layout === 'mosaic') : ?>
                                <?php
                                echo DSN_Mosaic::render(
                                    $slide['mosaic'],
                                    $kibana,
                                    $eager
                                );
                                ?>
                                <p class="dsn-slide-indicator dsn-slide-indicator--mosaic" aria-live="polite">
                                    <span class="dsn-slide-pos"><?php echo (int) $idx; ?></span> / 4
                                </p>
                            <?php else :
                                $type = $slide['type'];
                                $src = $type === 'kibana'
                                    ? $kibana . $slide['path']
                                    : $shiny . $slide['path'];
                                $state = $slide['state'] ?? 'loading';
                                $title = esc_attr($slide['title']);
                                $src_attr = esc_attr($src);
                                ?>
                                <p class="dsn-slide-caption"><?php echo esc_html($slide['caption']); ?></p>
                                <p class="dsn-slide-indicator" aria-live="polite">
                                    <span class="dsn-slide-pos"><?php echo (int) $idx; ?></span> / 4
                                </p>
                                <div class="dsn-embed-frame embed-wrapper">
                                    <?php if ($state === 'empty') : ?>
                                        <div class="dsn-state dsn-state--empty" role="status">Dado indisponível neste slide</div>
                                    <?php else : ?>
                                        <div class="dsn-state dsn-state--loading" hidden>Carregando visualização…</div>
                                        <div class="dsn-state dsn-state--error" hidden>Visualização temporariamente indisponível</div>
                                        <iframe
                                            class="dsn-embed-iframe"
                                            title="<?php echo $title; ?>"
                                            src="<?php echo $src_attr; ?>"
                                            loading="<?php echo $eager ? 'eager' : 'lazy'; ?>"
                                            referrerpolicy="no-referrer-when-downgrade"
                                            allow="fullscreen"
                                        ></iframe>
                                    <?php endif; ?>
                                </div>
                            <?php endif; ?>
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

    private static function kibana_embed_path(string $dashboard_id): string
    {
        return '/app/dashboards#/view/' . $dashboard_id
            . '?embed=true&_g=' . self::KIBANA_G
            . '&hide-filter-bar=true';
    }

    /**
     * @return array<int, array<string, mixed>>
     */
    private static function slides_for(string $page): array
    {
        if ($page === 'plataforma') {
            return [
                self::slide_plataforma_global_c(),
                self::slide_platform_mosaic_b(
                    'WhatsApp',
                    'whatsapp',
                    'WhatsApp · 2021–2024',
                    'O que circula no WhatsApp: tendencia, temas x ano e top temas?',
                    'kpis-whatsapp.json'
                ),
                self::slide_platform_mosaic_b(
                    'YouTube',
                    'youtube',
                    'YouTube · 2021–2024',
                    'O que circula no YouTube: tendencia, temas x ano e top temas?',
                    'kpis-youtube.json'
                ),
                self::slide_platform_mosaic_b(
                    'Facebook',
                    'facebook',
                    'Facebook · 2021–2024',
                    'O que circula no Facebook: tendencia, temas x ano e top temas?',
                    'kpis-facebook.json'
                ),
            ];
        }

        return [
            self::slide_global_mosaic_c(),
            self::slide_theme_mosaic_a(
                'eleicao',
                'Eleicao · 2021–2024',
                'Como a desinformacao sobre eleicao evolui no tempo e onde se concentra (plataforma/UF)?',
                'kpis-eleicao.json'
            ),
            self::slide_theme_mosaic_a(
                'vacinas',
                'Vacinas · 2021–2024',
                'Como a desinformacao sobre vacinas evolui no tempo e onde se concentra (plataforma/UF)?',
                'kpis-vacinas.json'
            ),
            self::slide_geo_mosaic_d(),
        ];
    }

    /** @return array<string, mixed> */
    private static function slide_global_mosaic_c(): array
    {
        $json = DSN_KPI::load_json('data/kpis-global-tema.json');
        $kpis = $json['kpis'] ?? self::fallback_kpis();
        return [
            'layout' => 'mosaic',
            'pattern' => 'C',
            'type' => 'mosaic',
            'state' => 'loading',
            'mosaic' => [
                'title' => 'Plataformas x Temas · 2021–2024',
                'question' => 'Como volume e engajamento se distribuem entre temas e plataformas (2021–2024)?',
                'pattern' => 'C',
                'slice' => ['dimension' => 'global', 'value' => 'all'],
                'kpis' => $kpis,
                'charts' => [
                    'dashboard' => [
                        'title' => 'Kibana — plataformas x temas (mosaico)',
                        'path' => DSN_Mosaic::embed_path('dsn-mosaic-t1'),
                    ],
                ],
            ],
        ];
    }

    /** @return array<string, mixed> */
    private static function slide_theme_mosaic_a(
        string $theme,
        string $title,
        string $question,
        string $kpi_file
    ): array {
        $json = DSN_KPI::load_json('data/' . $kpi_file);
        $kpis = $json['kpis'] ?? self::fallback_kpis();
        $slug = $theme;
        return [
            'layout' => 'mosaic',
            'pattern' => 'A',
            'type' => 'mosaic',
            'state' => 'loading',
            'mosaic' => [
                'title' => $title,
                'question' => $question,
                'pattern' => 'A',
                'slice' => ['dimension' => 'theme', 'value' => $theme],
                'kpis' => $kpis,
                'charts' => [
                    'dashboard' => [
                        'title' => "Kibana — {$theme} mosaico",
                        'path' => DSN_Mosaic::embed_path("dsn-mosaic-{$slug}"),
                    ],
                ],
            ],
        ];
    }

    /** @return array<string, mixed> */
    private static function slide_geo_mosaic_d(): array
    {
        $json = DSN_KPI::load_json('data/kpis-geo.json');
        $kpis = $json['kpis'] ?? self::fallback_kpis();
        return [
            'layout' => 'mosaic',
            'pattern' => 'D',
            'type' => 'mosaic',
            'state' => isset($_GET['dsn_empty']) ? 'empty' : 'loading',
            'mosaic' => [
                'title' => 'Distribuicao geografica · 2021–2024',
                'question' => 'Quais UFs e macrorregioes concentram eventos e como evoluem?',
                'pattern' => 'D',
                'slice' => ['dimension' => 'geo', 'value' => 'uf_region'],
                'kpis' => $kpis,
                'charts' => [
                    'dashboard' => [
                        'title' => 'Kibana — distribuicao geografica (mosaico)',
                        'path' => DSN_Mosaic::embed_path('dsn-mosaic-t4'),
                    ],
                ],
            ],
        ];
    }

    /** @return array<string, mixed> */
    private static function slide_plataforma_global_c(): array
    {
        $json = DSN_KPI::load_json('data/kpis-global-plataforma.json');
        $kpis = $json['kpis'] ?? self::fallback_kpis();
        return [
            'layout' => 'mosaic',
            'pattern' => 'C',
            'type' => 'mosaic',
            'state' => 'loading',
            'mosaic' => [
                'title' => 'Volume por plataforma · 2021–2024',
                'question' => 'Qual o share e a evolucao do volume total por plataforma?',
                'pattern' => 'C',
                'slice' => ['dimension' => 'global', 'value' => 'platform_angle'],
                'kpis' => $kpis,
                'charts' => [
                    'dashboard' => [
                        'title' => 'Kibana — volume por plataforma (mosaico)',
                        'path' => DSN_Mosaic::embed_path('dsn-mosaic-p1'),
                    ],
                ],
            ],
        ];
    }

    /** @return array<string, mixed> */
    private static function slide_platform_mosaic_b(
        string $platform,
        string $slug,
        string $title,
        string $question,
        string $kpi_file
    ): array {
        $json = DSN_KPI::load_json('data/' . $kpi_file);
        $kpis = $json['kpis'] ?? self::fallback_kpis();
        return [
            'layout' => 'mosaic',
            'pattern' => 'B',
            'type' => 'mosaic',
            'state' => 'loading',
            'mosaic' => [
                'title' => $title,
                'question' => $question,
                'pattern' => 'B',
                'slice' => ['dimension' => 'platform', 'value' => $platform],
                'kpis' => $kpis,
                'charts' => [
                    'dashboard' => [
                        'title' => "Kibana — {$platform} mosaico",
                        'path' => DSN_Mosaic::embed_path("dsn-mosaic-{$slug}"),
                    ],
                ],
            ],
        ];
    }

    /** @return array<int, array<string, mixed>> */
    private static function fallback_kpis(): array
    {
        return [
            [
                'id' => 'kpi-events',
                'label' => 'Eventos 2024',
                'value' => 0,
                'format' => 'int',
                'delta_pct' => null,
                'period_label' => 'vs 2023',
            ],
            [
                'id' => 'kpi-engagement',
                'label' => 'Engajamento soma 2024',
                'value' => 0,
                'format' => 'int',
                'delta_pct' => null,
                'period_label' => 'vs 2023',
            ],
            [
                'id' => 'kpi-share',
                'label' => 'Share',
                'value' => 0,
                'format' => 'pct',
                'delta_pct' => null,
                'period_label' => 'referencia',
            ],
            [
                'id' => 'kpi-leader',
                'label' => 'Destaque',
                'value' => '—',
                'format' => 'text',
                'delta_pct' => null,
                'period_label' => 'em 2024',
            ],
        ];
    }
}
