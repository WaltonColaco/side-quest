function PageTemplate({ title, children }) {
  return (
    <section className="template-shell" aria-label={`${title} page`}>
      <div className="template-panel">
        <h1 className="template-title">{title}</h1>
        {children ? <div className="template-body">{children}</div> : null}
      </div>
    </section>
  );
}

export default PageTemplate;
