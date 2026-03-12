# 🚀 Deployment Checklist

Complete guide to deploy your Air Quality Monitor dashboard to production.

## Phase 1: Pre-Deployment (Development)

### ✅ Environment Setup
- [ ] Node.js 18+ installed
- [ ] pnpm installed
- [ ] Project cloned/downloaded
- [ ] Dependencies installed: `pnpm install`

### ✅ Development Testing
- [ ] Development server runs: `pnpm dev`
- [ ] Dashboard loads at http://localhost:3000
- [ ] All 11 components visible
- [ ] Charts render correctly
- [ ] Mock data displays properly
- [ ] Responsive on mobile/tablet/desktop
- [ ] No console errors

### ✅ Code Quality
- [ ] TypeScript compilation passes
- [ ] No unused imports
- [ ] Components properly typed
- [ ] Mock data working as expected

---

## Phase 2: Backend Integration

### ✅ API Routes Setup
- [ ] Read `BACKEND_INTEGRATION.md`
- [ ] Python backend endpoints created
- [ ] POST `/api/predict` working
- [ ] GET `/api/metrics` working
- [ ] CORS configured on backend

### ✅ Environment Variables
- [ ] Create `.env.local` file
- [ ] Add `NEXT_PUBLIC_BACKEND_URL=<your-backend>`
- [ ] Test backend connection
- [ ] Verify API responses match expected format

### ✅ Frontend API Routes
- [ ] Update `/app/api/predict/route.ts`
- [ ] Update `/app/api/metrics/route.ts`
- [ ] Replace mock data with real backend calls
- [ ] Test API integration locally

### ✅ Data Flow Testing
- [ ] Real sensor data displays
- [ ] Real predictions show
- [ ] Real metrics display
- [ ] Charts update with real data
- [ ] No errors with real data

---

## Phase 3: Production Build

### ✅ Build Preparation
- [ ] Run `pnpm build` locally
- [ ] Build completes without errors
- [ ] No TypeScript errors
- [ ] No production warnings

### ✅ Build Testing
- [ ] Run `pnpm start` to test production build
- [ ] Dashboard loads correctly
- [ ] All features work
- [ ] Performance is acceptable
- [ ] No console errors

### ✅ Performance Verification
- [ ] Page load time < 3 seconds
- [ ] Charts render smoothly
- [ ] No memory leaks
- [ ] Images optimized

---

## Phase 4: Deployment Platform Setup

### ✅ Vercel Deployment (Recommended)

#### Option A: Git Integration
- [ ] Push code to GitHub/GitLab/Bitbucket
- [ ] Create Vercel account at vercel.com
- [ ] Import project from git
- [ ] Configure environment variables in Vercel dashboard
- [ ] Set `NEXT_PUBLIC_BACKEND_URL` in Vercel

#### Option B: CLI Deployment
- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Run `vercel login`
- [ ] Set up `.env` variables
- [ ] Run `vercel deploy`
- [ ] Add environment variables if prompted

### ✅ Environment Variables (Production)
- [ ] Set production backend URL
- [ ] Ensure HTTPS protocol
- [ ] Test connectivity to backend

### ✅ Other Hosting Platforms

If not using Vercel:
- [ ] Support for Node.js 18+
- [ ] Support for Next.js 16
- [ ] Environment variable configuration
- [ ] HTTPS/SSL certificates

---

## Phase 5: Domain & DNS

### ✅ Custom Domain (Optional)
- [ ] Domain registered
- [ ] DNS records configured
- [ ] SSL certificate enabled
- [ ] Domain points to deployment
- [ ] HTTPS working

### ✅ SSL Certificate
- [ ] HTTPS enabled
- [ ] Certificate valid
- [ ] No certificate warnings

---

## Phase 6: Pre-Launch Testing

### ✅ Production Environment Testing
- [ ] Access production URL
- [ ] Dashboard loads correctly
- [ ] All features functional
- [ ] Real data displays
- [ ] Charts render properly
- [ ] Recommendations show
- [ ] Responsive on all devices

### ✅ API Testing
- [ ] Predictions endpoint working
- [ ] Metrics endpoint working
- [ ] Backend connection stable
- [ ] Error handling works
- [ ] Rate limiting configured (if needed)

### ✅ Performance Testing
- [ ] Page load time acceptable
- [ ] Charts performance good
- [ ] No memory leaks
- [ ] Mobile performance acceptable
- [ ] API response times < 1 second

### ✅ Security Testing
- [ ] No sensitive data in frontend
- [ ] Environment variables secure
- [ ] Backend auth configured (if needed)
- [ ] CORS properly restricted
- [ ] XSS protection enabled
- [ ] CSRF protection enabled

### ✅ User Testing
- [ ] User can navigate dashboard
- [ ] All data displays correctly
- [ ] Charts are interactive
- [ ] Recommendations make sense
- [ ] Mobile experience smooth

---

## Phase 7: Monitoring & Maintenance

### ✅ Analytics Setup
- [ ] Vercel Analytics enabled
- [ ] Google Analytics configured (optional)
- [ ] Error tracking configured
- [ ] Performance monitoring active

### ✅ Logging
- [ ] Server logs accessible
- [ ] Error logs configured
- [ ] API request logging enabled
- [ ] Can track issues in production

### ✅ Backup & Recovery
- [ ] Source code backed up
- [ ] Database backups configured
- [ ] Recovery plan documented
- [ ] Disaster recovery tested

### ✅ Updates & Patches
- [ ] Dependencies up to date
- [ ] Security patches applied
- [ ] Next.js updated if needed
- [ ] React updated if needed

---

## Phase 8: Documentation & Handoff

### ✅ Documentation Updated
- [ ] README.md current
- [ ] Architecture documented
- [ ] Deployment steps documented
- [ ] Troubleshooting guide created
- [ ] Contact information included

### ✅ Team Knowledge Transfer
- [ ] Documentation shared
- [ ] Key contacts identified
- [ ] Access credentials shared securely
- [ ] Runbooks created
- [ ] Training completed (if needed)

### ✅ Monitoring Dashboards
- [ ] Alert thresholds set
- [ ] Dashboard metrics configured
- [ ] Performance baseline established
- [ ] On-call rotation set (if applicable)

---

## Deployment Command Checklists

### Vercel CLI Deployment
```bash
# 1. Prepare
pnpm install
pnpm build

# 2. Login
vercel login

# 3. Deploy
vercel deploy

# 4. Configure
# Follow prompts to set environment variables
```

### Docker Deployment (if applicable)
```bash
# Build Docker image
docker build -t air-quality-monitor .

# Run locally
docker run -p 3000:3000 air-quality-monitor

# Push to registry
docker push <your-registry>/air-quality-monitor
```

### Manual Server Deployment
```bash
# 1. Clone repo
git clone <repo>

# 2. Install
pnpm install

# 3. Build
pnpm build

# 4. Configure environment
cp .env.example .env.production
# Edit with production values

# 5. Run
pnpm start
# Or use PM2: pm2 start pnpm --name "aqi-dashboard" -- start
```

---

## Verification Checklist

After deployment, verify:

- [ ] Website accessible from production URL
- [ ] All pages load without errors
- [ ] Dashboard displays data correctly
- [ ] Charts render and are interactive
- [ ] Predictions update properly
- [ ] Recommendations display
- [ ] Mobile version works
- [ ] No console errors
- [ ] API calls succeed
- [ ] Backend integration working
- [ ] Performance acceptable
- [ ] Error pages work
- [ ] 404 page working
- [ ] Security headers present
- [ ] Analytics tracking working

---

## Troubleshooting Deployment Issues

### Build Failures
```bash
# Clean and rebuild
rm -rf .next node_modules pnpm-lock.yaml
pnpm install
pnpm build

# Check Node version
node --version  # Should be 18+
```

### Runtime Errors
1. Check production logs
2. Review environment variables
3. Verify backend connectivity
4. Check database connections
5. Review API responses

### Performance Issues
1. Enable caching
2. Optimize images
3. Use CDN for assets
4. Check database queries
5. Review bundle size

### Backend Connection Issues
1. Verify backend URL in env vars
2. Test backend directly
3. Check CORS configuration
4. Review network policies
5. Check authentication

---

## Rollback Procedure

If deployment has critical issues:

### Vercel
```bash
# View deployment history
vercel list

# Rollback to previous version
vercel rollback
```

### Manual Rollback
```bash
# Revert to previous commit
git revert <bad-commit-hash>
git push
# Redeploy previous version
```

---

## Post-Launch

### First Week
- [ ] Monitor error logs
- [ ] Check analytics
- [ ] Gather user feedback
- [ ] Fix any issues
- [ ] Optimize performance

### First Month
- [ ] Review metrics
- [ ] Update documentation
- [ ] Plan improvements
- [ ] Security audit
- [ ] Backup verification

### Ongoing
- [ ] Regular updates
- [ ] Security patches
- [ ] Performance monitoring
- [ ] User support
- [ ] Feature improvements

---

## Support & Contact

If deployment issues occur:

1. Check logs (Vercel/Server)
2. Review error messages
3. Consult troubleshooting guide
4. Check documentation
5. Contact backend team (for API issues)

---

## Final Sign-Off

Before going live:

- [ ] QA approval
- [ ] Security review passed
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Team trained
- [ ] Monitoring configured
- [ ] Backup verified
- [ ] Stakeholder approval

---

## 🎉 Deployment Complete!

Your Air Quality Monitor Dashboard is now live and serving users.

**Congratulations!**

For ongoing maintenance, refer to the monitoring section above and keep documentation up to date.

---

## Quick Reference

| Environment | URL | Variables |
|-------------|-----|-----------|
| Development | localhost:3000 | .env.local |
| Production | your-domain.com | Vercel/Server env |

---

Last Updated: [Deployment Date]
Next Review: [Review Date]
