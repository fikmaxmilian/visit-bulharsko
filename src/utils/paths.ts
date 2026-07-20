export function withBase(path = '/') {
  if (!path) return path;
  if (/^(https?:)?\/\//.test(path) || path.startsWith('mailto:') || path.startsWith('tel:') || path.startsWith('#')) {
    return path;
  }
  const base = import.meta.env.BASE_URL || '/';
  const cleanBase = base === '/' ? '' : base.replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBase}${cleanPath}` || '/';
}

export function canonicalUrl(path = '/') {
  const site = (import.meta.env.SITE || 'https://visitbulharsko.cz').replace(/\/$/, '');
  const base = import.meta.env.BASE_URL || '/';
  const cleanBase = base === '/' ? '' : base.replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${site}${cleanBase}${cleanPath}`;
}
