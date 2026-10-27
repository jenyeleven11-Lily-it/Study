import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

const links = ["Features", "Solutions", "Pricing", "About"];

const navEntrance = {
  initial: { y: -20, opacity: 0 },
  animate: { y: 0, opacity: 1 },
  transition: { duration: 0.8, ease: "easeOut" },
};

function NavLinks({ mobile = false, onNavigate }) {
  return links.map((item) => (
    <a
      key={item}
      href={`#${item.toLowerCase()}`}
      onClick={onNavigate}
      className={
        mobile
          ? "rounded-lg px-3 py-2 text-[15px] font-medium text-white/70 transition-colors hover:bg-white/10 hover:text-white"
          : "group relative text-[13px] font-medium text-white/70 transition-colors hover:text-white"
      }
    >
      {item}
      {!mobile && (
        <span className="absolute -bottom-1 left-0 h-0.5 w-0 bg-white transition-all duration-300 group-hover:w-full" />
      )}
    </a>
  ));
}

export default function KeloAutomationHero({ className = "" }) {
  const videoRef = useRef(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const slowVideo = () => {
      video.playbackRate = 0.6;
    };
    slowVideo();
    video.addEventListener("loadedmetadata", slowVideo);
    return () => video.removeEventListener("loadedmetadata", slowVideo);
  }, []);

  return (
    <section
      className={`kelo-hero relative flex min-h-[110vh] w-full flex-col overflow-hidden bg-black font-sans text-white ${className}`}
      aria-label="Kelo AI automation"
    >
      <video
        ref={videoRef}
        autoPlay
        muted
        loop
        playsInline
        className="absolute inset-0 z-0 h-full w-full object-cover"
        aria-hidden="true"
      >
        <source
          src="https://cdn.jiro.build/Kelo/Hero%201%20Video.mp4"
          type="video/mp4"
        />
      </video>
      <div className="absolute inset-0 z-[1] bg-black/20" aria-hidden="true" />

      <motion.nav
        {...navEntrance}
        className="absolute left-0 right-0 top-6 z-50 px-6"
        aria-label="Main navigation"
      >
        <div className="mx-auto flex max-w-4xl items-center justify-between rounded-full border border-white/10 bg-white/5 p-2 px-4 backdrop-blur-xl">
          <a href="#top" className="flex shrink-0 items-center" aria-label="Kelo home">
            <img
              src="https://cdn.jiro.build/Kelo/Kelo%20White.svg"
              alt="Kelo Logo"
              referrerPolicy="no-referrer"
              className="h-[22px] w-auto"
            />
          </a>

          <div className="hidden items-center gap-5 md:flex">
            <NavLinks />
          </div>

          <div className="hidden items-center gap-2 md:flex">
            <a
              href="#login"
              className="px-2 py-1.5 text-[13px] font-medium text-white/70 transition-colors hover:text-white"
            >
              Log in
            </a>
            <a
              href="#get-started"
              className="rounded-full bg-white px-4 py-1.5 text-[13px] font-semibold text-black transition-all hover:scale-105 hover:bg-white/90 active:scale-95"
            >
              Get Started
            </a>
          </div>

          <button
            type="button"
            className="flex h-8 w-8 flex-col items-center justify-center gap-[5px] md:hidden"
            aria-label={menuOpen ? "Close menu" : "Toggle menu"}
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <span
              className={`block h-[2px] w-5 bg-white transition-all duration-300 ${menuOpen ? "translate-y-[7px] rotate-45" : ""}`}
            />
            <span
              className={`block h-[2px] w-5 bg-white transition-all duration-300 ${menuOpen ? "opacity-0" : ""}`}
            />
            <span
              className={`block h-[2px] w-5 bg-white transition-all duration-300 ${menuOpen ? "-translate-y-[7px] -rotate-45" : ""}`}
            />
          </button>
        </div>

        <AnimatePresence>
          {menuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="mt-2 flex flex-col gap-3 rounded-2xl border border-white/10 bg-black/60 p-4 backdrop-blur-xl md:hidden"
            >
              <NavLinks mobile onNavigate={() => setMenuOpen(false)} />
              <div className="mt-1 flex flex-col gap-2 border-t border-white/10 pt-3">
                <a
                  href="#login"
                  onClick={() => setMenuOpen(false)}
                  className="rounded-lg px-3 py-2 text-left text-[15px] font-medium text-white/70 transition-colors hover:bg-white/10 hover:text-white"
                >
                  Log in
                </a>
                <a
                  href="#get-started"
                  onClick={() => setMenuOpen(false)}
                  className="rounded-full bg-white px-5 py-2.5 text-center text-[15px] font-semibold text-black transition-all hover:bg-white/90"
                >
                  Get Started
                </a>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.nav>

      <div className="relative z-10 flex flex-1 flex-col items-center justify-center px-6 pb-16 pt-[148px] text-center">
        <div className="pointer-events-none absolute left-1/2 top-1/2 z-0 h-[600px] w-[600px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-white/5 blur-[120px]" />
        <div className="relative z-10 flex w-full flex-col items-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
            className="group mb-6 flex cursor-default items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 backdrop-blur-md"
          >
            <span className="flex h-2 w-2 animate-pulse rounded-full bg-white" />
            <span className="text-xs font-semibold uppercase tracking-[0.2em] text-white/80 transition-colors group-hover:text-white">
              New: AI-Powered Sales Engine
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: "easeOut" }}
            className="mb-6 mt-0 max-w-4xl text-center text-5xl font-semibold leading-[1.05] tracking-[-0.03em] text-white md:text-6xl lg:text-[72px]"
          >
            Power Your Business with
            <br />
            <span className="bg-gradient-to-r from-white via-white/80 to-white/60 bg-clip-text text-transparent">
              AI Intelligence
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
            className="mb-10 max-w-[520px] text-center text-base leading-relaxed text-white/70 md:text-lg"
          >
            Leverage advanced AI algorithms to optimize your operations, enhance
            decision-making, and drive sustainable growth for your enterprise.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3, ease: "easeOut" }}
            className="flex flex-col items-center gap-4"
          >
            <div className="group relative">
              <div className="absolute -inset-1 rounded-full bg-white/20 opacity-0 blur-xl transition duration-500 group-hover:opacity-100" />
              <a
                href="#get-started"
                className="relative flex scale-100 items-center justify-center overflow-hidden rounded-full bg-white px-10 py-4 text-base font-semibold text-black shadow-2xl transition-all hover:scale-105 hover:bg-white/90 active:scale-95"
              >
                Get 14 Days Free Trial
              </a>
            </div>
            <div className="flex items-center gap-2 text-sm text-white/50">
              <svg
                className="h-4 w-4 text-white/40"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  d="M5 13l4 4L19 7"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <span>No Credit Card Required</span>
            </div>
          </motion.div>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
        className="absolute bottom-10 left-1/2 z-10 flex -translate-x-1/2 flex-col items-center gap-2"
      >
        <span className="text-[10px] font-semibold uppercase tracking-[0.3em] text-white/30">
          Scroll
        </span>
        <span className="h-12 w-px bg-gradient-to-b from-white/40 to-transparent" />
      </motion.div>
    </section>
  );
}
