function PageTemplate({ title }) {
  return (
    <section className="template-shell" aria-label={`${title} page`}>
      <div className="template-panel">
        <h1 className="template-title">{title}</h1>
      </div>
    </section>
  );
}

export default PageTemplate;
