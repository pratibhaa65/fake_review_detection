const Footer = () => {
  return (
    <footer className="bg-slate-950 text-gray-400">
      <div className="max-w-7xl mx-auto px-6 py-6 text-center">
        <p className="text-sm text-gray-400">
          © {new Date().getFullYear()} Fake Review Detection System | Built for Trust
        </p>
      </div>
    </footer>
  );
};

export default Footer;
