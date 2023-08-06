#![allow(non_snake_case)]

use std::{time::Instant, sync::{RwLock, Arc}};

use prometheus::{opts, HistogramVec, IntCounterVec, Registry};

use rocket::{fairing::{Info, Kind, Fairing}, Request, Data, Response};

/// Prometheus Rocket Metrics
///
/// This library provides a way to collect Prometheus metrics for HTTP requests in a Rocket web service.
/// It includes a `PrometheusMetrics` struct for managing the metrics, and an `ArcRwLockPrometheus` struct
/// that can be used as a `Fairing` in Rocket to collect and update the metrics for each request.
///
/// # Example Usage
///
/// ```rust
/// use rocket::{Rocket, Build};
/// use std::{sync::{RwLock, Arc}};
/// use rocket::{ get, routes };
/// use rocket_metric_collector::metrics::metrics::{ArcRwLockPrometheus, PrometheusMetrics};
///
/// fn rocket() -> Rocket<Build> {
///     let prometheus = Arc::new(RwLock::new(PrometheusMetrics::new("my_app")));
///     let prometheus_fairing = ArcRwLockPrometheus::new(prometheus.clone());
///
///     Rocket::build()
///         .attach(prometheus_fairing)
///         .mount("/", routes![index])
/// }
///
/// #[get("/")]
/// fn index() -> &'static str {
///     "Hello, world!"
/// }
///
/// fn main() {
///     rocket().launch();
/// }
/// ```
///
/// This example sets up a Rocket web service with Prometheus metrics collection. The `ArcRwLockPrometheus`
/// fairing is attached to the Rocket instance, and the `PrometheusMetrics` instance is created with the
/// desired namespace ("my_app" in this case). The `index` route is defined as a simple endpoint that
/// returns a greeting message. When the web service receives a request, the `on_request` method is called,
/// and when a response is sent, the `on_response` method is called. The metrics are incremented and observed
/// accordingly based on the endpoint, method, and status of the request and response.
pub struct PrometheusMetrics {
    http_requests_total: IntCounterVec,
    http_requests_duration_seconds: HistogramVec,
    registry: Registry,
}

impl PrometheusMetrics {
    /// Creates a new instance of PrometheusMetrics.
    ///
    /// # Arguments
    ///
    /// * `namespace` - The namespace for the metrics.
    ///
    /// # Returns
    ///
    /// A new instance of PrometheusMetrics.
    pub fn new(namespace: &str) -> Self {
        let registry = Registry::new();

        let http_requests_total_opts = opts!(
            "http_requests_total",
            "Total number of HTTP requests"
        ).namespace(namespace);
        let http_requests_total = IntCounterVec::new(
            http_requests_total_opts,
            &["endpoint", "method", "status"]
        ).unwrap();
        let http_requests_duration_seconds_opts = opts!(
            "http_requests_duration_seconds",
            "HTTP request duration in seconds for all requests"
        ).namespace(namespace);
        let http_requests_duration_seconds = HistogramVec::new(
            http_requests_duration_seconds_opts.into(),
            &["endpoint", "method", "status"]
        ).unwrap();

        registry.register(Box::new(http_requests_total.clone())).unwrap();
        registry.register(Box::new(http_requests_duration_seconds.clone())).unwrap();

        Self {
            http_requests_total,
            http_requests_duration_seconds,
            registry,
        }
    }

    /// Returns a reference to the Prometheus registry.
    pub const fn registry(&self) -> &Registry {
        &self.registry
    }

    /// Returns a reference to the HTTP request counter metric.
    pub fn http_requests_total(&self) -> &IntCounterVec {
        &self.http_requests_total
    }

    /// Returns a reference to the HTTP request duration metric.
    pub fn http_requests_duration_seconds(&self) -> &HistogramVec {
        &self.http_requests_duration_seconds
    }
}

impl Clone for PrometheusMetrics {
    fn clone(&self) -> Self {
        Self {
            http_requests_total: self.http_requests_total.clone(),
            http_requests_duration_seconds: self.http_requests_duration_seconds.clone(),
            registry: self.registry.clone(),
        }
    }
}

/// Struct representing the start time of a timer.
#[derive(Copy, Clone)]
struct TimerStart(Option<Instant>);

/// Trait for providing a clone function for Arc<RwLock<PrometheusMetrics>>.
pub trait ArcRwLockPrometheusTrait {
    type ArcRwLock;
    fn clone(&self) -> Arc<RwLock<PrometheusMetrics>>;
}

/// Struct for managing Prometheus metrics with an Arc<RwLock<PrometheusMetrics>>.
pub struct ArcRwLockPrometheus {
    pub rwLock: Arc<RwLock<PrometheusMetrics>>,
}

impl ArcRwLockPrometheus {
    /// Creates a new instance of ArcRwLockPrometheus.
    ///
    /// # Arguments
    ///
    /// * `prometheus` - The Arc<RwLock<PrometheusMetrics>> instance to be managed.
    ///
    /// # Returns
    ///
    /// A new instance of ArcRwLockPrometheus.
    pub fn new(prometheus: Arc<RwLock<PrometheusMetrics>>) -> Self {
        Self {
            rwLock: prometheus,
        }
    }
}

impl Clone for ArcRwLockPrometheus {
    fn clone(&self) -> Self {
        Self {
            rwLock: Arc::clone(&self.rwLock),
        }
    }
}

impl ArcRwLockPrometheusTrait for ArcRwLockPrometheus {
    type ArcRwLock = Arc<RwLock<PrometheusMetrics>>;

    fn clone(&self) -> Arc<RwLock<PrometheusMetrics>> {
        Arc::clone(&self.rwLock)
    }
}

#[rocket::async_trait]
impl Fairing for ArcRwLockPrometheus {
    /// Returns information about the fairing.
    fn info(&self) -> Info {
        Info {
            name: "Prometheus metric collection",
            kind: Kind::Request | Kind::Response,
        }
    }

    /// Called when a request is received.
    async fn on_request(&self, req: &mut Request<'_>, _: &mut Data<'_>) {
        req.local_cache(|| TimerStart(Some(Instant::now())));
    }

    /// Called when a response is sent.
    async fn on_response<'r>(&self, req: &'r Request<'_>, response: &mut Response<'r>) {
        if req.route().is_none() {
            return;
        }

        let endpoint = req.route().unwrap().uri.as_str();
        let method = req.method().as_str();
        let status = response.status().code.to_string();
        self.rwLock
            .read()
            .unwrap()
            .http_requests_total
            .with_label_values(&[endpoint, method, status.as_str()])
            .inc();

        let start_time = req.local_cache(|| TimerStart(None));
        if let Some(duration) = start_time.0.map(|st| st.elapsed()) {
            let duration_secs = duration.as_secs_f64();
            self.rwLock
                .read()
                .unwrap()
                .http_requests_duration_seconds
                .with_label_values(&[endpoint, method, status.as_str()])
                .observe(duration_secs);
        }
    }
}
