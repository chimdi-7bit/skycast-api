import { useState, useEffect } from 'react'; // Import React state and side-effect hooks
import './App.css'; // Import minimal existing styles

function App() { // Main Weather Dashboard component
  const [city, setCity] = useState('Lagos'); // State for city name input/search
  const [searchInput, setSearchInput] = useState('Lagos'); // State for controlled input field
  const [weatherData, setWeatherData] = useState<any>(null); // Current weather data from backend
  const [forecastData, setForecastData] = useState<any>(null); // 5-day forecast data from backend
  const [newsData, setNewsData] = useState<any[]>([]); // News feed articles from backend
  const [exchangeData, setExchangeData] = useState<any>(null); // Currency rates from backend
  const [loading, setLoading] = useState(true); // Global loading indicator state

  // Define the base URL for the backend API, allowing for environment-based configuration during deployment
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'; // Default to localhost if no ENV is set

  // Function to fetch all dashboard metrics in parallel from the FastAPI backend
  const fetchDashboardData = async (targetCity: string) => { // Async data aggregator
    setLoading(true); // Trigger loading overlay
    try { // Orchestrate parallel API requests
      const [weatherRes, forecastRes, newsRes, exchangeRes] = await Promise.all([
        fetch(`${API_BASE_URL}/weather?city=${targetCity}`), // Fetch localized weather and astro data
        fetch(`${API_BASE_URL}/forecast?city=${targetCity}`), // Fetch extended outlook
        fetch(`${API_BASE_URL}/news`), // Fetch curated news intel
        fetch(`${API_BASE_URL}/exchange-rate?base=NGN`) // Fetch Naira-based currency conversions
      ]);

      // Parse JSON responses
      const weather = await weatherRes.json(); // Decode weather
      const forecast = await forecastRes.json(); // Decode forecast
      const news = await newsRes.json(); // Decode news
      const exchange = await exchangeRes.json(); // Decode exchange

      // Validate responses and update state
      if (!weather.detail) setWeatherData(weather); // Persist if no error
      if (!forecast.detail) setForecastData(forecast); // Persist if no error
      if (!news.detail) setNewsData(news.articles?.slice(0, 3) || []); // Persist top 3 headlines
      if (!exchange.detail) setExchangeData(exchange); // Persist if no error
      
    } catch (err) { // Log sync errors to the console
      console.error("Dashboard Sync Failed:", err); // Error diagnostics
    } finally { // Cleanup loading state
      setLoading(false); // Remove loading overlay
    }
  }; // End of fetch function

  // Initial dashboard population when the app first mounts
  useEffect(() => { // Startup initialization
    fetchDashboardData(city); // Request data for default location (Lagos)
  }, []); // Run exactly once

  // Handler for searching new locations in Nigeria
  const handleSearch = (e: React.FormEvent) => { // Search form event handler
    e.preventDefault(); // Stop default form navigation
    if (searchInput.trim()) { // Validate that input is not empty
      setCity(searchInput); // Update active city state
      fetchDashboardData(searchInput); // Request new data for the target city
    }
  }; // End of search handler

  // Helper function to map weather descriptions to Material Icons
  const getWeatherIcon = (description: string) => { // Icon mapping utility
    const desc = description?.toLowerCase() || ''; // Standardize input
    if (desc.includes('cloud')) return 'partly_cloudy_day'; // Cloud icon
    if (desc.includes('rain')) return 'rainy'; // Rain icon
    if (desc.includes('clear')) return 'sunny'; // Clear sky icon
    if (desc.includes('storm')) return 'thunderstorm'; // Storm icon
    return 'cloud'; // Default fallback icon
  }; // End of icon helper

  if (loading) return ( // Render premium loading screen during data retrieval
    <div className="h-screen w-full flex items-center justify-center bg-background text-primary font-bold text-2xl animate-pulse">
      SYNCING STRATOSPHERIC INTELLIGENCE...
    </div>
  ); // End of loading check

  return ( // Main application UI layout
    <>
      {/* Top Navigation Bar: Branded header with city search */}
      <header className="fixed top-0 w-full z-50 flex justify-between items-center px-8 h-20 bg-cyan-950/60 backdrop-blur-3xl shadow-[0_0_30px_rgba(0,0,0,0.4)] border-b border-white/10 text-on-surface">
        <div className="text-2xl font-black tracking-tighter text-primary">AtmosSync</div> {/* Application Logo */}
        <div className="flex-1 max-w-md mx-8 text-on-surface"> {/* Search input container */}
          <form onSubmit={handleSearch} className="relative flex items-center"> {/* Form wrapper for search */}
            <span className="material-symbols-outlined absolute left-3 text-slate-400">search</span> {/* Search icon */}
            <input 
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)} // Bind input to state
              className="w-full bg-surface-container-lowest/60 border-none border-b border-outline-variant/30 focus:border-primary focus:ring-0 text-sm font-label py-2 pl-10 transition-all rounded-lg text-on-surface" 
              placeholder="Search coordinates or city in Nigeria..." 
              type="text"
            /> {/* Search text field */}
          </form> {/* End of search form */}
        </div> {/* End of search container */}
        <nav className="flex items-center gap-6"> {/* Secondary actions navigation */}
          <button className="material-symbols-outlined text-slate-400 hover:text-primary transition-colors duration-300">notifications</button> {/* Alert trigger */}
          <button className="material-symbols-outlined text-slate-400 hover:text-primary transition-colors duration-300">settings</button> {/* App configuration */}
        </nav> {/* End of nav section */}
      </header> {/* End of header */}

      <main className="pt-28 pb-20 px-8 max-w-[1440px] mx-auto text-on-surface"> {/* Main layout canvas */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 text-on-surface"> {/* Responsive 12-column Bento Grid */}
          
          {/* Main Weather Card: Feature module for local conditions */}
          <section className="md:col-span-8 glass-panel rounded-3xl p-8 flex flex-col justify-between min-h-[420px] relative overflow-hidden group text-on-surface">
            <div className="absolute -right-12 -top-12 opacity-20 group-hover:opacity-30 transition-opacity"> {/* Background decorative icon */}
              <span className="material-symbols-outlined text-[320px] text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>
                {getWeatherIcon(weatherData?.weather?.[0]?.description)}
              </span> {/* Large faint background icon */}
            </div> {/* End of background icon decoration */}
            <div className="relative z-10 text-on-surface"> {/* Foreground content layer */}
              <div className="flex justify-between items-start text-on-surface"> {/* Metadata header row */}
                <div className="text-on-surface"> {/* Location labels */}
                  <h2 className="font-label text-xs uppercase tracking-[0.2em] text-primary mb-1">Local Conditions</h2> {/* Section label */}
                  <p className="text-3xl font-bold tracking-tight text-on-surface">{weatherData?.name || city}, NG</p> {/* City and country display */}
                </div> {/* End of location labels */}
                <div className="text-right"> {/* Grid status badge */}
                  <span className="inline-block px-3 py-1 bg-surface-variant/40 rounded-full text-[10px] font-label uppercase tracking-widest text-primary border border-white/10">Precision Grid Active</span> {/* Operational status */}
                </div> {/* End of badge container */}
              </div> {/* End of header row */}
              <div className="flex items-end gap-8 mt-12 text-on-surface"> {/* High-impact weather data display */}
                <div className="flex items-center gap-4 text-on-surface"> {/* Icon and temperature group */}
                  <span className="material-symbols-outlined text-8xl text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>
                    {getWeatherIcon(weatherData?.weather?.[0]?.description)}
                  </span> {/* Large feature weather icon */}
                  <div className="flex flex-col text-on-surface"> {/* Temperature and description vertical stack */}
                    <span className="text-[7rem] font-bold leading-none tracking-tighter text-glow text-on-surface">
                      {weatherData?.main?.temp ? Math.round(weatherData.main.temp) : '--'}°
                    </span> {/* Massive glowing temperature */}
                    <span className="font-label text-lg text-on-surface-variant capitalize">{weatherData?.weather?.[0]?.description || 'Syncing...'}</span> {/* Sky condition text */}
                  </div> {/* End of stack */}
                </div> {/* End of icon group */}
              </div> {/* End of feature data section */}
            </div> {/* End of upper content block */}
            <div className="relative z-10 grid grid-cols-3 gap-8 mt-auto pt-8 border-t border-white/10 text-on-surface"> {/* Secondary stats row */}
              <div className="flex flex-col"> {/* Humidity display block */}
                <span className="font-label text-[10px] uppercase tracking-widest text-slate-400 mb-1">Humidity</span> {/* Label */}
                <div className="flex items-center gap-2"> {/* Icon and value pair */}
                  <span className="material-symbols-outlined text-primary text-sm">humidity_mid</span> {/* Metric icon */}
                  <span className="text-xl font-medium">{weatherData?.main?.humidity || '0'}%</span> {/* Numerical value */}
                </div> {/* End of pair */}
              </div> {/* End of humidity block */}
              <div className="flex flex-col"> {/* Wind display block */}
                <span className="font-label text-[10px] uppercase tracking-widest text-slate-400 mb-1">Wind Speed</span> {/* Label */}
                <div className="flex items-center gap-2"> {/* Icon and value pair */}
                  <span className="material-symbols-outlined text-primary text-sm">air</span> {/* Metric icon */}
                  <span className="text-xl font-medium">{weatherData?.wind?.speed || '0'} m/s</span> {/* Numerical value */}
                </div> {/* End of pair */}
              </div> {/* End of wind block */}
              <div className="flex flex-col"> {/* Pressure display block */}
                <span className="font-label text-[10px] uppercase tracking-widest text-slate-400 mb-1">Pressure</span> {/* Label */}
                <div className="flex items-center gap-2"> {/* Icon and value pair */}
                  <span className="material-symbols-outlined text-primary text-sm">compress</span> {/* Metric icon */}
                  <span className="text-xl font-medium">{weatherData?.main?.pressure || '0'} hPa</span> {/* Numerical value */}
                </div> {/* End of pair */}
              </div> {/* End of pressure block */}
            </div> {/* End of secondary stats row */}
          </section> {/* End of main conditions card */}

          {/* Celestial Hub Card: Astronomical intelligence module */}
          <section className="md:col-span-4 glass-panel rounded-3xl p-6 flex flex-col text-on-surface">
            <h3 className="font-label text-[10px] uppercase tracking-widest text-primary mb-6 flex items-center gap-2"> {/* Header with moon icon */}
              <span className="material-symbols-outlined text-xs">nights_stay</span>
              Celestial Hub
            </h3> {/* End of hub header */}
            <div className="flex-1 flex flex-col gap-6 text-on-surface"> {/* Container for celestial events */}
              <div className="relative h-24 flex items-center justify-center text-on-surface"> {/* Visual representation of the sun's path */}
                <div className="absolute inset-0 border-b-2 border-white/10 rounded-[100%] h-32 -top-16"></div> {/* Arc graphic */}
                <div className="flex justify-between w-full px-4 items-end pb-2 text-on-surface"> {/* Sunrise and Sunset data points */}
                  <div className="text-center"> {/* Sunrise block */}
                    <span className="material-symbols-outlined text-tertiary mb-1">wb_twilight</span> {/* Rise icon */}
                    <p className="font-label text-[10px] text-slate-400">SUNRISE</p> {/* Metric label */}
                    <p className="text-sm font-bold text-on-surface">{weatherData?.astro?.sunrise || '--:--'}</p> {/* Formatted time from backend */}
                  </div> {/* End of sunrise */}
                  <div className="text-center"> {/* Sunset block */}
                    <span className="material-symbols-outlined text-tertiary-fixed-dim mb-1">wb_sunny</span> {/* Set icon */}
                    <p className="font-label text-[10px] text-slate-400">SUNSET</p> {/* Metric label */}
                    <p className="text-sm font-bold text-on-surface">{weatherData?.astro?.sunset || '--:--'}</p> {/* Formatted time from backend */}
                  </div> {/* End of sunset */}
                </div> {/* End of data row */}
              </div> {/* End of sun path visual */}
              <div className="bg-surface-container-lowest/40 rounded-2xl p-4 mt-auto border border-white/5 text-on-surface"> {/* Narrative moon status container */}
                <div className="flex items-center gap-3 mb-2"> {/* Status header with icon */}
                  <span className="material-symbols-outlined text-primary">brightness_3</span> {/* Moon phase icon */}
                  <span className="font-label text-xs uppercase tracking-wider">Moon Status</span> {/* Section title */}
                </div> {/* End of moon header */}
                <p className="text-sm text-on-surface-variant leading-relaxed"> {/* Dynamic descriptive moon position text */}
                  {weatherData?.astro?.moon_status || 'Waiting for lunar sync...'}
                </p> {/* End of descriptive text */}
              </div> {/* End of moon narrative block */}
            </div> {/* End of hub content container */}
          </section> {/* End of Celestial Hub card */}

          {/* Chronos Forecast Card: Extended temporal weather outlook */}
          <section className="md:col-span-12 glass-panel rounded-3xl p-6 text-on-surface">
            <h3 className="font-label text-[10px] uppercase tracking-widest text-primary mb-6">Chronos Forecast • 120 Hours</h3> {/* Heading */}
            <div className="flex justify-between items-center overflow-x-auto pb-2 gap-4 text-on-surface"> {/* Horizontal scrollable forecast container */}
              {forecastData?.list?.filter((_: any, i: number) => i % 8 === 0).map((day: any, index: number) => ( // Map every 24th hour block
                <div key={index} className={`flex flex-col items-center min-w-[100px] p-4 rounded-2xl border transition-all ${index === 0 ? 'bg-white/10 border-white/10 shadow-lg' : 'hover:bg-white/5 border-transparent'}`}>
                  <span className="font-label text-[10px] text-slate-400 mb-3">
                    {new Date(day.dt * 1000).toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase()}
                  </span> {/* Formatted day label */}
                  <span className="material-symbols-outlined text-primary mb-3">
                    {getWeatherIcon(day.weather?.[0]?.description)}
                  </span> {/* Daily weather icon */}
                  <span className="text-lg font-bold text-on-surface">{Math.round(day.main?.temp || 0)}°</span> {/* Daily predicted temp */}
                </div> // End of forecast item
              ))} {/* End of forecast map */}
            </div> {/* End of scrollable row */}
          </section> {/* End of forecast card */}

          {/* Currency Intelligence Card: Naira-centric financial hub */}
          <section className="md:col-span-5 glass-panel rounded-3xl p-6 text-on-surface">
            <h3 className="font-label text-[10px] uppercase tracking-widest text-primary mb-6">Currency Intelligence (1 NGN Base)</h3> {/* Section heading */}
            <div className="space-y-4 text-on-surface"> {/* Vertical list of currency metrics */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors"> {/* USD Row */}
                <div className="flex items-center gap-3"> {/* Icon and label group */}
                  <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center font-bold text-[10px]">USD</div> {/* Currency code */}
                  <span className="font-label text-sm text-on-surface">US Dollar</span> {/* Full currency name */}
                </div> {/* End group */}
                <span className="text-sm font-bold text-primary">{exchangeData?.conversion_rates?.USD?.toFixed(5) || '0.00000'}</span> {/* High-precision rate */}
              </div> {/* End of USD row */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors"> {/* EUR Row */}
                <div className="flex items-center gap-3"> {/* Icon and label group */}
                  <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center font-bold text-[10px]">EUR</div> {/* Currency code */}
                  <span className="font-label text-sm text-on-surface">Euro</span> {/* Full currency name */}
                </div> {/* End group */}
                <span className="text-sm font-bold text-primary">{exchangeData?.conversion_rates?.EUR?.toFixed(5) || '0.00000'}</span> {/* High-precision rate */}
              </div> {/* End of EUR row */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors"> {/* GBP Row */}
                <div className="flex items-center gap-3"> {/* Icon and label group */}
                  <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center font-bold text-[10px]">GBP</div> {/* Currency code */}
                  <span className="font-label text-sm text-on-surface">British Pound</span> {/* Full currency name */}
                </div> {/* End group */}
                <span className="text-sm font-bold text-primary">{exchangeData?.conversion_rates?.GBP?.toFixed(5) || '0.00000'}</span> {/* High-precision rate */}
              </div> {/* End of GBP row */}
            </div> {/* End of currency list container */}
          </section> {/* End of Currency Hub card */}

          {/* World Intel Feed Card: Curated global headline streams */}
          <section className="md:col-span-7 glass-panel rounded-3xl p-6 text-on-surface">
            <h3 className="font-label text-[10px] uppercase tracking-widest text-primary mb-6">World Intel Feed</h3> {/* Heading label */}
            <div className="space-y-6 text-on-surface"> {/* Feed of headline items */}
              {newsData.length > 0 ? newsData.map((article, idx) => ( // Map through news articles from the state
                <div key={idx} className="group cursor-pointer"> {/* Individual news story entry */}
                  <p className="text-sm font-bold group-hover:text-primary transition-colors line-clamp-1 mb-1 text-on-surface">{article.title}</p> {/* Truncated headline with hover effect */}
                  <div className="flex items-center gap-2"> {/* Source and time metadata row */}
                    <span className="text-[10px] font-label text-slate-400 uppercase">{article.source.name}</span> {/* News publisher name */}
                    <span className="w-1 h-1 rounded-full bg-white/20"></span> {/* Vertical metadata separator dot */}
                    <span className="text-[10px] font-label text-slate-400">Live Insight</span> {/* Feed status indicator */}
                  </div> {/* End of metadata row */}
                </div> // End of news item entry
              )) : (
                <p className="text-sm text-on-surface-variant italic">Retrieving latest intelligence streams...</p>
              )}
            </div> {/* End of intel feed container */}
          </section> {/* End of World Intel card */}

        </div> {/* End of Bento Grid layout */}
      </main> {/* End of main canvas */}

      {/* Global Dashboard Footer: System status and temporal metrics */}
      <footer className="fixed bottom-0 w-full z-50 flex justify-between items-center px-6 py-3 bg-slate-950/80 backdrop-blur-3xl border-t border-white/10">
        <div className="flex items-center gap-2"> {/* System status group */}
          <span className="relative flex h-2 w-2"> {/* Multi-layer pulsing status indicator */}
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span> {/* Ping outer ring */}
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span> {/* Solid status core */}
          </span> {/* End of indicator */}
          <span className="font-mono text-[10px] uppercase tracking-widest text-primary">Sync Status: Active | Precision Grid v4.0</span> {/* Version and state labels */}
        </div> {/* End of system status block */}
        <div className="flex gap-4"> {/* Tertiary navigation links */}
          <a className="font-mono text-[10px] uppercase tracking-widest text-slate-400 hover:text-primary transition-colors" href="#">System Logs</a> {/* Technical log link */}
          <a className="font-mono text-[10px] uppercase tracking-widest text-slate-400 hover:text-primary transition-colors" href="#">Network Health</a> {/* Infrastructure health link */}
        </div> {/* End of navigation links */}
        <div className="font-mono text-[10px] text-slate-400 uppercase tracking-widest"> {/* Live time display */}
          {new Date().toLocaleTimeString()} LOCAL {/* Real-time system clock formatted for UI */}
        </div> {/* End of time block */}
      </footer> {/* End of footer layout */}
    </>
  ); // End of JSX return
}

export default App; // Export AtmosSync Dashboard as the primary application entry point
