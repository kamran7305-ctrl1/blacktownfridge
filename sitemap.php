<?php
/**
 * XML sitemap served at /sitemap.xml (see the rewrite rule in .htaccess).
 *
 * - Static pages come from sitemap-static.xml (the file you edit when a new
 *   page is added). lastmod is taken from the page file's modified time.
 * - Published blog posts are added from the database, with lastmod from the
 *   post's updated_at (or created_at).
 * - If the database is unavailable the static pages are still served, so the
 *   sitemap never returns an error because of the blog.
 */
$base = 'https://fridgerepairblacktown.com.au';

function sm_fail_safe(string $staticXml): void
{
    if (!defined('SITEMAP_COMPLETE')) {
        while (ob_get_level() > 0) {
            ob_end_clean();
        }
        if (!headers_sent()) {
            http_response_code(200);
            header('Content-Type: application/xml; charset=UTF-8');
        }
        echo $staticXml;
    }
}

/** Map a canonical page URL to the file that renders it. */
function sm_file_for(string $loc, string $base): ?string
{
    $path = trim(substr($loc, strlen($base)), '/');
    if ($path === '') {
        return __DIR__ . '/index.html';
    }
    if ($path === 'blog') {
        return __DIR__ . '/blog.php';
    }
    $file = __DIR__ . '/' . $path . '.html';
    return is_file($file) ? $file : null;
}

function sm_entry(string $loc, ?int $mtime, string $changefreq, string $priority): string
{
    $xml = "    <url>\n        <loc>" . htmlspecialchars($loc, ENT_XML1) . "</loc>\n";
    if ($mtime) {
        $xml .= '        <lastmod>' . gmdate('Y-m-d', $mtime) . "</lastmod>\n";
    }
    return $xml . "        <changefreq>$changefreq</changefreq>\n        <priority>$priority</priority>\n    </url>\n";
}

// 1. Static pages
$static = @file_get_contents(__DIR__ . '/sitemap-static.xml');
$entries = '';
$staticLocs = [];
if ($static !== false && preg_match_all('#<url>(.*?)</url>#s', $static, $blocks)) {
    foreach ($blocks[1] as $block) {
        if (!preg_match('#<loc>(.*?)</loc>#', $block, $m)) {
            continue;
        }
        $loc = html_entity_decode(trim($m[1]));
        $freq = preg_match('#<changefreq>(.*?)</changefreq>#', $block, $f) ? $f[1] : 'monthly';
        $prio = preg_match('#<priority>(.*?)</priority>#', $block, $p) ? $p[1] : '0.8';
        $file = sm_file_for($loc, $base);
        $mtime = $file ? filemtime($file) : null;
        $staticLocs[$loc] = ['freq' => $freq, 'prio' => $prio, 'mtime' => $mtime];
    }
}
$head = '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
$foot = '</urlset>' . "\n";
$buildStatic = function (array $locs, ?int $blogMtime = null) use ($base): string {
    $out = '';
    foreach ($locs as $loc => $d) {
        $mtime = $d['mtime'];
        if ($loc === $base . '/blog/' && $blogMtime) {
            $mtime = max((int) $mtime, $blogMtime);
        }
        $out .= sm_entry($loc, $mtime, $d['freq'], $d['prio']);
    }
    return $out;
};
$staticXml = $head . $buildStatic($staticLocs) . $foot;
register_shutdown_function('sm_fail_safe', $staticXml);

// 2. Blog posts (database). config.php exits with a message if the database
// is unreachable; the shutdown handler above then serves the static sitemap.
ob_start();
define('SKIP_SESSION', true);
require __DIR__ . '/admin/config.php';
$posts = [];
$blogMtime = null;
try {
    $rows = $pdo->query("SELECT slug, created_at, updated_at FROM blog_posts WHERE status = 'published' ORDER BY created_at DESC LIMIT 1000")->fetchAll();
    foreach ($rows as $row) {
        $ts = strtotime($row['updated_at'] ?: $row['created_at']);
        $posts[] = sm_entry($base . '/blog/' . rawurlencode($row['slug']), $ts ?: null, 'monthly', '0.7');
        $blogMtime = max((int) $blogMtime, (int) $ts);
    }
} catch (Throwable $e) {
    $posts = [];
}
ob_end_clean();

header('Content-Type: application/xml; charset=UTF-8');
header('Cache-Control: public, max-age=3600');
echo $head . $buildStatic($staticLocs, $blogMtime) . implode('', $posts) . $foot;
define('SITEMAP_COMPLETE', true);
