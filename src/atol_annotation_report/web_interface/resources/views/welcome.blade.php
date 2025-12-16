<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>Upload Files</title>
    <style>
        :root {
            --bg1: #1e3c72;
            --bg2: #2a5298;
            --bg3: #ff7e5f;
            --bg4: #feb47b;
            --text: #f7fafc;
        }
        * {
            box-sizing: border-box
        }

        html,
        body {
            height: 100%;
            margin: 0;
            color: var(--text);
            font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background:
                radial-gradient(1200px 800px at 10% 10%, rgba(255, 255, 255, .08), transparent 60%),
                radial-gradient(900px 700px at 90% 20%, rgba(255, 255, 255, .06), transparent 60%),
                linear-gradient(120deg, var(--bg1), var(--bg2), var(--bg3), var(--bg4));
            background-size: 200% 200%;
            animation: shift 18s ease-in-out infinite;
        }

        .page-container {
            display: flex;
            gap: 40px;
            max-width: 1200px;
            margin: 20px;
            align-items: center;
        }

        .left-section {
            flex: 0 0 400px;
            margin-top: -40px; /* Offset to visually balance with the right side */
        }

        .images-container {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            justify-content: center;
        }

        .explanation-text {
            background: rgba(255, 255, 255, .12);
            border: 1px solid rgba(255, 255, 255, .25);
            border-radius: 18px;
            padding: 20px;
            line-height: 1.6;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        @keyframes shift {

            0%,
            100% {
                background-position: 0% 50%
            }

            50% {
                background-position: 100% 50%
            }
        }

        .card {
            width: min(92vw, 540px);
            padding: 28px;
            border-radius: 18px;
            background: rgba(255, 255, 255, .12);
            border: 1px solid rgba(255, 255, 255, .25);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, .25), inset 0 1px 0 rgba(255, 255, 255, .2);
        }

        h1 {
            margin: 0 0 6px;
            font-size: clamp(22px, 3.4vw, 30px)
        }

        p.lead {
            margin: 0 0 22px;
            opacity: .9
        }

        form {
            display: grid;
            gap: 16px
        }

        .field {
            display: grid;
            gap: 8px
        }

        .two-columns {
            display: flex;
            gap: 12px;
        }

        label {
            font-size: .95rem
        }

        .file-input {
            border: 1px dashed rgba(255, 255, 255, .35);
            border-radius: 14px;
            padding: 16px;
            background: rgba(255, 255, 255, .07)
        }

        input[type="file"] {
            width: 100%;
            color: #fff
        }

        .actions {
            display: grid;
            gap: 10px;
            margin-top: 6px
        }

        button {
            border: 0;
            border-radius: 12px;
            padding: 14px 18px;
            font-weight: 700;
            cursor: pointer;
            color: #0b1220;
            background: #fff;
            box-shadow: 0 8px 20px rgba(0, 0, 0, .2)
        }

        .modal {
            position: fixed;
            inset: 0;
            display: none;
            place-items: center;
            background: rgba(10, 14, 30, .38);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            z-index: 50;
        }

        .modal.show {
            display: grid
        }

        .modal-card {
            width: min(92vw, 420px);
            padding: 24px;
            border-radius: 16px;
            background: rgba(255, 255, 255, .14);
            border: 1px solid rgba(255, 255, 255, .28);
            box-shadow: 0 10px 28px rgba(0, 0, 0, .35)
        }

        .title {
            margin: 0 0 6px;
            font-weight: 700
        }

        .msg {
            margin: 6px 0 14px;
            line-height: 1.4
        }

        .spinner {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            border: 5px solid rgba(255, 255, 255, .35);
            border-top-color: #fff;
            animation: spin 1s linear infinite;
            margin: 8px auto 14px;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg)
            }
        }

        .status-ok {
            border-left: 4px solid #22c55e;
            padding-left: 10px
        }

        .status-err {
            border-left: 4px solid #ef4444;
            padding-left: 10px
        }

        .status-run {
            border-left: 4px solid #f59e0b;
            padding-left: 10px
        }

        .row {
            display: flex;
            gap: 8px;
            justify-content: flex-end;
            margin-top: 8px
        }

        .ghost {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, .6);
            color: #fff
        }

        select option {
            background-color: #2a5298;
            color: white;
        }

        select {
            background-color: rgba(255, 255, 255, 0.1) !important;
        }

        .template-download {
            display: inline-block;
            padding: 8px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            float: right;
            margin-top: 24px;
        }

        .template-download:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.5);
        }

        .field-with-template {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 15px;
        }
        /* Links in bottom left corner */
        .bottom-links {
            position: fixed;
            bottom: 20px;
            left: 20px;
            display: flex;
            gap: 20px;
            z-index: 40;
        }

        .bottom-link {
            color: white;
            text-decoration: underline;
            transition: opacity 0.3s ease;
        }

        .bottom-link:hover {
            opacity: 0.8;
        }

        /* Team modal */
        #teamModal {
            display: none;
            position: fixed;
            inset: 0;
            place-items: center;
            background: rgba(10, 14, 30, 0.38);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            z-index: 60;
        }

        #teamModal.show {
            display: grid;
        }

        .team-modal-card {
            width: min(92vw, 500px);
            padding: 24px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.28);
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
        }

        .team-list {
            list-style: none;
            padding: 0;
            margin: 20px 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }

        .team-list li {
            padding: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 6px;
        }
    </style>
</head>

<body>
    <div class="page-container">
        <div class="left-section">
            <div class="images-container">
                <img src="/images/biohackathon.png" alt="BioHackathon Logo" style="width: 150px; height: auto;">
                <img src="/images/elixier.png" alt="ELIXIR Logo" style="width: 150px; height: auto;">
            </div>
            <div class="explanation-text">
                After uploading your files, the pipeline will extract features from the gff file using AGAT v.1.5.0
                then gffread will use the assembly and annotation to get the translated proteins, which will be used to assess completeness with BUSCO v5.8.2 and OMArk v0.3.1.
                A pdf file containing all metadata and calculated stats together with BUSCO and OMArk plots will be downloaded.
            </div>
        </div>
        <div class="card" role="main" aria-labelledby="title">
        <h1 id="title">Streamlining FAIR Metadata for Biodiversity Genome Annotations</h1>
        <p class="lead">Upload your files and click <strong>Submit</strong></p>

        <form id="uploadForm">
            <div class="field">
                <label for="species_name">Species Name</label>
                <input id="species_name" name="species_name" type="text" required style="width: 100%; padding: 8px; border-radius: 8px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.3); color: white;">
            </div>

            <div class="field">
                <label for="file_one">GFF File</label>
                <div class="file-input"><input id="file_one" name="file_one" type="file" required></div>
            </div>

            <div class="field two-columns">
                <div style="flex:1;">
                    <label for="busco_results">BUSCO Results File</label>
                    <div class="file-input"><input id="busco_results" name="busco_results" type="file"></div>
                </div>
                <div style="flex:1;">
                    <label for="omark_results">OMArk Results File</label>
                    <div class="file-input"><input id="omark_results" name="omark_results" type="file"></div>
                </div>
            </div>

            <div class="field field-with-template">
                <div style="flex-grow: 1;">
                    <label for="file_two">Metadata CSV File</label>
                    <div class="file-input"><input id="file_two" name="file_two" type="file" required></div>
                </div>
                <a href="/templates/metadata_template.csv" download class="template-download">
                    📥 Download Metadata template
                </a>
            </div>

            <div class="actions">
                <button type="submit">Submit</button>

            </div>
        </form>
    </div>

    <div id="modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
        <div class="modal-card">
            <h3 id="modalTitle" class="title">Running…</h3>
            <div id="modalBody" class="msg status-run">
                <div class="spinner" aria-hidden="true"></div>
                Please wait while processing your files.
            </div>
            <div class="row">
                <button id="closeBtn" type="button" class="ghost" style="display:none;">Close</button>
            </div>
        </div>
    </div>

    <script>
        (() => {
            const form = document.getElementById('uploadForm');
            const modal = document.getElementById('modal');
            const title = document.getElementById('modalTitle');
            const body = document.getElementById('modalBody');
            const closeBtn = document.getElementById('closeBtn');

            // for test

            const EXTERNAL_API_URL = '/upload';

            function openModal(state, message) {
                if (!modal.classList.contains('show')) modal.classList.add('show');
                closeBtn.style.display = (state === 'success' || state === 'error') ? 'inline-block' : 'none';

                    if (state === 'running') {
                        title.textContent = 'Running…';
                        body.className = 'msg status-run';
                        body.innerHTML =
                            `<div class="spinner" aria-hidden="true"></div>${message || 'Please wait while processing your files.'}`;
                    } else if (state === 'success') {
                        title.textContent = 'Success';
                        body.className = 'msg status-ok';
                        // allow small HTML (e.g. download link)
                        body.innerHTML = message || 'Done!';
                    } else if (state === 'error') {
                        title.textContent = 'Failed';
                        body.className = 'msg status-err';
                        body.textContent = message || 'The external API reported failure.';
                    }
            }

            function closeModal() {
                modal.classList.remove('show');
            }
            closeBtn.addEventListener('click', closeModal);

            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const f1 = document.getElementById('file_one').files[0];
                const f2 = document.getElementById('file_two').files[0];
                const busco = document.getElementById('busco_results') ? document.getElementById('busco_results').files[0] : null;
                const omark = document.getElementById('omark_results') ? document.getElementById('omark_results').files[0] : null;

                if (!f1 || !f2) {
                    openModal('error', 'Please select the GFF file and the Metadata CSV file before submitting.');
                    return;
                }

                const data = new FormData();
                data.append('file_one', f1);
                data.append('file_two', f2);
                if (busco) data.append('busco_results', busco);
                if (omark) data.append('omark_results', omark);

                openModal('running');

                try {
                    // include CSRF token from meta tag (required by Laravel)
                    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
                    const headers = { 'Accept': 'application/json' };
                    if (csrfMeta) headers['X-CSRF-TOKEN'] = csrfMeta.getAttribute('content');

                    let res;
                    try {
                        res = await fetch(EXTERNAL_API_URL, { method: 'POST', body: data, headers: headers });
                    } catch (networkErr) {
                        openModal('error', 'Network error: ' + (networkErr && networkErr.message ? networkErr.message : 'request failed'));
                        return;
                    }

                    // try to parse JSON, but fall back to text for error messages
                    let body;
                    try {
                        body = await res.json();
                    } catch (err) {
                        body = await res.text();
                    }

                    if (!res.ok) {
                        // if server returned JSON with message, show it, otherwise show text
                        const msg = (body && body.message) ? body.message : (typeof body === 'string' ? body : JSON.stringify(body));
                        openModal('error', `API error: ${res.status} ${res.statusText} - ${msg}`);
                        return;
                    }

                    if (body && body.status === 'success' && body.output_url) {
                        openModal('success', `Completed successfully. <br><a href="${body.output_url}" download>Download results</a>`);
                        return;
                    }

                    openModal('error', `Unexpected response: ${JSON.stringify(body)}`);
                } catch (err) {
                    openModal('error', 'Network error or the request was blocked.');
                }
            });

            // Team modal functionality
            const teamModal = document.getElementById('teamModal');
            const teamCloseBtn = document.getElementById('teamCloseBtn');
            const teamLink = document.getElementById('teamLink');

            teamLink.addEventListener('click', (e) => {
                e.preventDefault();
                teamModal.classList.add('show');
            });

            teamCloseBtn.addEventListener('click', () => {
                teamModal.classList.remove('show');
            });

            // Close modal when clicking outside
            teamModal.addEventListener('click', (e) => {
                if (e.target === teamModal) {
                    teamModal.classList.remove('show');
                }
            });
        })();
    </script>

    <!-- Bottom right links -->
    <div class="bottom-links">
        <a href="#" class="bottom-link" id="teamLink">Team</a>
        <a href="https://github.com/fairtracks" class="bottom-link" target="_blank">GitHub</a>
    </div>

    <!-- Team Modal -->
    <div id="teamModal" class="modal">
        <div class="team-modal-card">
            <h3 class="title">Our Team</h3>
            <ul class="team-list">
                <li>Sveinung Gundersen</li>
                <li>David Swarbreck</li>
                <li>Clara Emery</li>
                <li>Alice Dennis</li>
                <li>Tom Harrop</li>
                <li>Qussai Abbas</li>
                <li>Ole K. Tørresen</li>
                <li>Anna Lazar</li>
                <li>Arne Becker</li>
                <li>Keiler Collier</li>
                <li>Keeva</li>
                <li>Tiff</li>
                <li>Jia</li>
                <li>Steven</li>
                <li>Jane</li>
                <li>Emily</li>
            </ul>
            <div class="row">
                <button id="teamCloseBtn" type="button" class="ghost">Close</button>
            </div>
        </div>
    </div>
</body>

</html>
