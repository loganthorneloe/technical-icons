/* Offline asset browser. Every download uses the bytes of a standalone repository file. */
(() => {
  'use strict';
  const {icons, categories, assets, assetCount} = window.ICON_LIBRARY;
  const $ = id => document.getElementById(id);
  const styles = {illustrated: 'Illustrated', compact: 'Compact', brand: 'Flat mark'};
  const state = {category: 'all', query: '', background: 'dark', style: 'all', size: 'fit', selected: null, detailStyle: null};
  const backgrounds = {dark: '#101527', paper: '#e9ddc7', white: '#ffffff'};
  const styleFor = icon => state.style !== 'all' && icon.renditions[state.style] ? state.style : icon.style;
  const fileFor = (icon, style = styleFor(icon)) => {
    const rendition = icon.renditions[style];
    return rendition.tones[state.background === 'dark' ? 'ivory' : 'ink'] || rendition.file;
  };
  const imageUrl = file => 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(assets[file]);
  const available = icon => state.style === 'all' || Boolean(icon.renditions[state.style]);
  $('total').textContent = `${icons.length} icon concepts`;
  $('category-total').textContent = `${Object.keys(categories).length} categories`;
  $('style-summary').textContent = `${assetCount} SVG files, including styles and tones`;

  function renderCategories() {
    const eligible = icons.filter(available);
    $('categories').replaceChildren(...[['all', 'All icons'], ...Object.entries(categories)].map(([key, label]) => {
      const button = document.createElement('button'); button.type = 'button'; button.dataset.category = key;
      button.append(document.createTextNode(label));
      const count = document.createElement('span'); count.textContent = key === 'all' ? eligible.length : eligible.filter(icon => icon.category === key).length;
      button.append(count);
      button.addEventListener('click', () => {state.category = key; render();});
      return button;
    }));
  }

  function render() {
    const terms = state.query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const filtered = icons.filter(icon => available(icon) && (state.category === 'all' || icon.category === state.category) && terms.every(term => `${icon.name} ${icon.id} ${icon.description} ${icon.tags.join(' ')} ${categories[icon.category]}`.toLowerCase().includes(term)));
    $('collection-title').textContent = state.category === 'all' ? 'All icons' : categories[state.category];
    $('count').textContent = `${filtered.length} ${filtered.length === 1 ? 'icon' : 'icons'}`;
    $('empty').hidden = filtered.length > 0;
    document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === state.category)));
    const fragment = document.createDocumentFragment();
    for (const icon of filtered) {
      const style = styleFor(icon);
      const button = document.createElement('button'); button.type = 'button'; button.className = 'icon-card';
      button.setAttribute('aria-label', `View ${icon.name}`);
      const stage = document.createElement('span'); stage.className = 'icon-stage';
      const img = document.createElement('img'); img.src = imageUrl(fileFor(icon, style)); img.alt = ''; img.loading = 'lazy'; img.dataset.style = style;
      img.width = icon.renditions[style].size; img.height = icon.renditions[style].size;
      if (state.size !== 'fit') {img.style.width = `${state.size}px`; img.style.height = `${state.size}px`;}
      stage.append(img);
      const label = document.createElement('span'); label.className = 'icon-label';
      const name = document.createElement('strong'); name.textContent = icon.name;
      const category = document.createElement('small'); category.textContent = `${categories[icon.category]} · ${styles[style]}`;
      label.append(name, category); button.append(stage, label);
      button.addEventListener('click', () => openDetail(icon)); fragment.append(button);
    }
    $('grid').replaceChildren(fragment);
  }

  function renderDetail() {
    const icon = state.selected, style = state.detailStyle, rendition = icon.renditions[style], file = fileFor(icon, style);
    $('detail-name').textContent = icon.name;
    $('detail-category').textContent = categories[icon.category].toUpperCase();
    $('detail-description').textContent = icon.description;
    $('detail-path').textContent = file;
    const img = document.createElement('img'); img.src = imageUrl(file); img.alt = icon.description; img.className = 'detail-art';
    const samples = document.createElement('div'); samples.className = 'size-samples'; samples.setAttribute('aria-label', 'Actual size previews');
    for (const size of style === 'illustrated' ? [48, 96, 128] : [24, 32, 48]) {
      const sample = document.createElement('span'), small = document.createElement('img'), label = document.createElement('small');
      small.src = img.src; small.alt = `${icon.name} at ${size} pixels`; small.width = size; small.height = size;
      label.textContent = `${size}px`; sample.append(small, label); samples.append(sample);
    }
    $('detail-preview').replaceChildren(img, samples);
    $('detail-tags').replaceChildren(...icon.tags.map(tag => {const span = document.createElement('span'); span.textContent = tag; return span;}));
    $('detail-format').textContent = `SVG · ${rendition.size} × ${rendition.size} grid · transparent background`;
    $('detail-usage').textContent = `Recommended at ${rendition.recommendedMinSize}px or larger. ${style === 'illustrated' ? 'Use the illustrated version for slides and larger diagrams.' : 'Designed for smaller diagrams and website elements.'} Download and copy use the style and tone shown here.`;
    $('detail-attribution').hidden = !icon.attribution;
    $('detail-attribution').replaceChildren();
    if (icon.attribution) {
      const source = document.createElement('a'); source.href = icon.source; source.textContent = icon.provider || 'Font Awesome Free'; source.target = '_blank'; source.rel = 'noopener noreferrer';
      $('detail-attribution').append(source, document.createTextNode(` · ${icon.license}. Source and treatment details are included in the SVG metadata.`));
    }
    $('copy-status').textContent = ''; $('copy-fallback').hidden = true;
  }

  function openDetail(icon) {
    state.selected = icon; state.detailStyle = styleFor(icon);
    $('detail-style').replaceChildren(...Object.keys(icon.renditions).map(style => new Option(styles[style], style)));
    $('detail-style').value = state.detailStyle;
    $('detail-style').disabled = Object.keys(icon.renditions).length === 1;
    renderDetail(); $('detail').showModal();
  }

  $('search').addEventListener('input', event => {state.query = event.target.value; render();});
  $('style-filter').addEventListener('change', event => {state.style = event.target.value; renderCategories(); render();});
  $('size-filter').addEventListener('change', event => {state.size = event.target.value; render();});
  $('detail-style').addEventListener('change', event => {state.detailStyle = event.target.value; renderDetail();});
  $('reset').addEventListener('click', () => {state.query = ''; state.category = 'all'; state.style = 'all'; $('search').value = ''; $('style-filter').value = 'all'; renderCategories(); render();});
  document.querySelectorAll('[data-bg]').forEach(button => button.addEventListener('click', () => {
    state.background = button.dataset.bg;
    document.documentElement.style.setProperty('--preview', backgrounds[state.background]);
    document.documentElement.style.setProperty('--preview-label', state.background === 'dark' ? '#9fa1a9' : '#304654');
    document.querySelectorAll('[data-bg]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    render();
  }));
  $('close').addEventListener('click', () => $('detail').close());
  $('detail').addEventListener('click', event => {if (event.target === $('detail')) {const r = $('detail').getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) $('detail').close();}});
  $('download').addEventListener('click', () => {
    if (!state.selected) return;
    const file = fileFor(state.selected, state.detailStyle);
    const url = URL.createObjectURL(new Blob([assets[file]], {type: 'image/svg+xml;charset=utf-8'}));
    const link = document.createElement('a'); link.href = url;
    link.download = `${state.selected.id}${file.startsWith('variants/') ? '-' + file.split('/')[1] : ''}.svg`;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  $('copy').addEventListener('click', async () => {
    if (!state.selected) return;
    const content = assets[fileFor(state.selected, state.detailStyle)];
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(content);
      $('copy-status').textContent = 'SVG code copied.';
    } catch {
      $('copy-fallback').hidden = false; $('copy-fallback').value = content;
      $('copy-fallback').focus(); $('copy-fallback').select();
      $('copy-status').textContent = 'Copy the selected SVG code with ⌘C / Ctrl+C.';
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !$('detail').open && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {event.preventDefault(); $('search').focus();}
  });
  renderCategories(); render();
})();
