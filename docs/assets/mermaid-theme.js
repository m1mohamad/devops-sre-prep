window.addEventListener('load', () => {
  if (window.mermaid) {
    window.mermaid.initialize({
      startOnLoad: true,
      theme: document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'default',
      themeVariables: {
        primaryColor: '#3f51b5',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#283593',
        lineColor: '#607d8b',
        secondaryColor: '#ffecb3',
        tertiaryColor: '#eef2ff',
        fontFamily: 'Inter, system-ui, sans-serif'
      }
    });
  }
});
