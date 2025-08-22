You want to deploy **NGINX Ingress Controller on GKE** (instead of using the default GCE ingress). This is very common if you need features that GCP’s built-in ingress doesn’t support (e.g., custom NGINX annotations, fine-grained rewrites, gRPC, canary routing).

Here’s the step-by-step guide:

---

## 🚀 Install NGINX Ingress Controller on GKE

### 1. Add Helm repo

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

### 2. Create namespace

```bash
kubectl create namespace ingress-nginx
```

### 3. Install ingress-nginx

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux
```

This will:

* Deploy **nginx ingress controller pods**.
* Create a **LoadBalancer service** for external access.

---

## 🔎 Verify Installation

Check pods:

```bash
kubectl get pods -n ingress-nginx
```

Check service (look for EXTERNAL-IP):

```bash
kubectl get svc -n ingress-nginx
```

You should see something like:

```
NAME                                 TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                      AGE
ingress-nginx-controller             LoadBalancer   10.8.12.23     34.120.55.101    80:31432/TCP,443:31433/TCP   2m
```

➡️ That `EXTERNAL-IP` is the public IP for your ingress.

---

## ✅ Example Ingress with NGINX

### Deploy Echo Server
```yml

kind: Deployment
metadata:
  name: echo-server-deployment
spec:
  replicas: 2 # Number of echo server instances
  selector:
    matchLabels:
      app: echo-server
  template:
    metadata:
      labels:
        app: echo-server
    spec:
      containers:
      - name: echo-server
        image: gcr.io/google_containers/echoserver:1.9 # Your Docker image
        ports:
        - containerPort: 8080 # Port your echo server listens on

---
apiVersion: v1
kind: Service
metadata:
  name: echo-server-service
spec:
  selector:
    app: echo-server
  ports:
  - protocol: TCP
    port: 80 # External port for the service
    targetPort: 8080 # Port on the pods
  type: NodePort # Or ClusterIP for internal access, NodePort for specific node port

```
Apply it:

```bash
kubectl apply -f echo.yaml
```



Now create an Ingress that routes to two services:

```yaml
kind: Ingress
metadata:
  name: nginx-multipath-ingress
  namespace: default
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - http:
      paths:
      - path: /ui
        pathType: Prefix
        backend:
          service:
            name: echo-server-service
            port:
              number: 80
      - path: /echo
        pathType: Prefix
        backend:
          service:
            name: echo-server-service
            port:
              number: 80
```

Apply it:

```bash
kubectl apply -f ingress.yaml
```

Then test:

```bash
curl http://<NGINX-INGRESS-EXTERNAL-IP>/echo
curl http://<NGINX-INGRESS-EXTERNAL-IP>/ui
```

---

⚡ Pro tip: If you want **internal ingress only** (within VPC), you can set:

```bash
--set controller.service.annotations."cloud\.google\.com/load-balancer-type"="Internal"
```

during Helm install.

---

Enabling **TLS/HTTPS with Let’s Encrypt (cert-manager + NGINX Ingress)** on **GKE**.

This is the standard way to automate certificate management in Kubernetes.

---

## ⚡ Steps: HTTPS with Let’s Encrypt + NGINX Ingress (on GKE)

### 1. Install cert-manager

```bash
kubectl create namespace cert-manager

kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.1/cert-manager.yaml
```

(Check [latest release](https://github.com/cert-manager/cert-manager/releases) if needed.)

Verify:

```bash
kubectl get pods -n cert-manager
```

You should see `cert-manager`, `cert-manager-webhook`, and `cert-manager-cainjector` running.

---

### 2. Create a ClusterIssuer (for Let’s Encrypt)

This tells cert-manager how to request certs from Let’s Encrypt.

👉 For production (real certs):

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: your-email@example.com          # REQUIRED
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod-secret
    solvers:
    - http01:
        ingress:
          class: nginx
```

👉 For staging (testing, avoids rate limits):

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    email: your-email@example.com
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-staging-secret
    solvers:
    - http01:
        ingress:
          class: nginx
```

Apply:

```bash
kubectl apply -f cluster-issuer.yaml
```

---

### 3. Update your Ingress to request a certificate

Example ingress with TLS (for domain `myapp.example.com`):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-https-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"   # or letsencrypt-staging
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls       # cert-manager will create this Secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

---

### 4. Apply ingress

```bash
kubectl apply -f ingress-https.yaml
```

---

### 5. Wait for certificate issuance

Check cert-manager events:

```bash
kubectl describe certificate myapp-tls
kubectl get certificate,secret
```

Once successful, cert-manager will create a **Kubernetes TLS Secret** (`myapp-tls`) with your certificate + private key, and NGINX Ingress will serve HTTPS automatically 🎉.

---

### 6. Test HTTPS

Make sure your DNS (`myapp.example.com`) points to the NGINX ingress external IP.
Then test:

```bash
curl -v https://myapp.example.com
```

---

✅ Done! You now have **auto-renewing Let’s Encrypt certificates** managed by cert-manager + NGINX on GKE.

---

Nice one 🚀 You’re asking about **Contour** and its `HTTPProxy` resource on **GKE**.
Contour is an **alternative ingress controller** to NGINX, built by VMware, that uses **Envoy** as the data plane. It introduces the `HTTPProxy` CRD instead of the standard `Ingress`.

Here’s how to install **Contour on GKE** and enable `HTTPProxy`:

---

## ⚡ Step 1: Install Contour

Contour provides official deployment YAMLs:

```bash
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml
```

This will:

* Install Contour in the `projectcontour` namespace.
* Deploy Envoy as a **LoadBalancer Service** (default public IP).
* Install the `HTTPProxy` CRD.

Verify:

```bash
kubectl get pods -n projectcontour
```

You should see something like:

```
contour-xxxxx   Running
envoy-xxxxx     Running
```

Check the LoadBalancer service (this gives your ingress IP):

```bash
kubectl get svc -n projectcontour
```

Example:

```
NAME     TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                      AGE
envoy    LoadBalancer   10.12.45.67    34.123.45.89    80:32000/TCP,443:32001/TCP   2m
```

---

## ⚡ Step 2: Deploy Services

Example:
`frontend-service` (port 80) and `backend-service` (port 8080).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - port: 8080
      targetPort: 8080
```

---

## ⚡ Step 3: Create an HTTPProxy

Now define a `HTTPProxy` that routes multiple paths:

```yaml
apiVersion: projectcontour.io/v1
kind: HTTPProxy
metadata:
  name: multipath-proxy
  namespace: default
spec:
  virtualhost:
    fqdn: myapp.example.com
  routes:
    - conditions:
        - prefix: /frontend
      services:
        - name: frontend-service
          port: 80
    - conditions:
        - prefix: /backend
      services:
        - name: backend-service
          port: 8080
```

Apply it:

```bash
kubectl apply -f httpproxy.yaml
```

---

## ⚡ Step 4: Test Access

1. Point your DNS (`myapp.example.com`) → the Envoy service `EXTERNAL-IP`.
   Or edit `/etc/hosts` locally:

   ```
   34.123.45.89   myapp.example.com
   ```

2. Test:

   ```bash
   curl http://myapp.example.com/frontend
   curl http://myapp.example.com/backend
   ```

---

## ✅ Optional: Enable TLS with Let’s Encrypt

Contour integrates with **cert-manager** just like NGINX. You’d create a `ClusterIssuer` and then update `HTTPProxy`:

```yaml
spec:
  virtualhost:
    fqdn: myapp.example.com
    tls:
      secretName: myapp-tls
```

cert-manager will fill the TLS secret, and Envoy (via Contour) will serve HTTPS.

---




