#!/usr/bin/env node
/**
 * OpenClaw Obsidian Sync Server
 * A secure file sync server for two-way synchronization
 */

import { createServer } from 'http';
import { readFile, writeFile, readdir, stat } from 'fs/promises';
import { join, resolve, parse } from 'path';
import { existsSync } from 'fs';

// Configuration
const CONFIG = {
    port: parseInt(process.env.SYNC_PORT || '18790'),
    bind: process.env.SYNC_BIND || 'localhost',
    workspace: process.env.SYNC_WORKSPACE || '/data/clawdbot',
    token: process.env.SYNC_TOKEN,
    allowedPaths: (process.env.SYNC_ALLOWED_PATHS || 'notes,memory').split(',')
};

// Validate token
if (!CONFIG.token) {
    console.error('SYNC_TOKEN environment variable is required');
    process.exit(1);
}

// Security: Prevent path traversal
function isSafePath(basePath, targetPath) {
    const resolved = resolve(basePath, targetPath);
    return resolved.startsWith(basePath) && !resolved.includes('..');
}

// Parse JSON body
async function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                resolve(body ? JSON.parse(body) : {});
            } catch (e) {
                reject(new Error('Invalid JSON'));
            }
        });
        req.on('error', reject);
    });
}

// Send JSON response
function sendJson(res, status, data) {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
}

// Auth middleware
function authenticate(req) {
    const auth = req.headers.authorization;
    return auth === `Bearer ${CONFIG.token}`;
}

// Handle sync requests
async function handleSync(req, res) {
    const url = new URL(req.url, `http://${CONFIG.bind}:${CONFIG.port}`);
    const path = url.searchParams.get('path') || '';
    const method = req.method;

    // Check auth
    if (!authenticate(req)) {
        return sendJson(res, 401, { error: 'Unauthorized' });
    }

    // Build full path
    const fullPath = join(CONFIG.workspace, path);

    // Security check
    if (!isSafePath(CONFIG.workspace, path)) {
        return sendJson(res, 403, { error: 'Path not allowed' });
    }

    try {
        // GET /sync/status
        if (method === 'GET' && url.pathname === '/sync/status') {
            return sendJson(res, 200, { 
                status: 'ok',
                workspace: CONFIG.workspace,
                allowedPaths: CONFIG.allowedPaths
            });
        }

        // GET /sync/list
        if (method === 'GET' && url.pathname === '/sync/list') {
            const items = await readdir(fullPath, { withFileTypes: true });
            const files = items
                .filter(i => i.isFile() && i.name.endsWith('.md'))
                .map(i => ({
                    name: i.name,
                    isDirectory: false,
                    size: 0,
                    modified: null
                }));
            return sendJson(res, 200, { files });
        }

        // GET /sync/read
        if (method === 'GET' && url.pathname === '/sync/read') {
            const content = await readFile(fullPath, 'utf-8');
            const stats = await stat(fullPath);
            return sendJson(res, 200, {
                content,
                metadata: {
                    size: stats.size,
                    modified: stats.mtime.toISOString()
                }
            });
        }

        // POST /sync/write
        if (method === 'POST' && url.pathname === '/sync/write') {
            const body = await parseBody(req);
            if (!body.content) {
                return sendJson(res, 400, { error: 'content required' });
            }
            await writeFile(fullPath, body.content, 'utf-8');
            return sendJson(res, 200, { success: true });
        }

        // 404
        sendJson(res, 404, { error: 'Not found' });

    } catch (err) {
        console.error('Sync error:', err);
        sendJson(res, err.code === 'ENOENT' ? 404 : 500, { 
            error: err.message 
        });
    }
}

// Create and start server
const server = createServer(handleSync);

server.listen(CONFIG.port, CONFIG.bind, () => {
    console.log(`OpenClaw Sync Server running on ${CONFIG.bind}:${CONFIG.port}`);
    console.log(`Workspace: ${CONFIG.workspace}`);
    console.log(`Allowed paths: ${CONFIG.allowedPaths.join(', ')}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    server.close();
    process.exit(0);
});
