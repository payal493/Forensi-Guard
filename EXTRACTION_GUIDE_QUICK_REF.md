# Android Data Extraction Guide - Quick Reference

## 🚀 Quick Access
**URL**: http://127.0.0.1:5000/extraction-guide

## ✨ Key Features at a Glance

| Feature | Description |
|---------|-------------|
| 📱 Simplified View | Toggle for non-technical users |
| 📋 Step Cards | 6 numbered instruction cards |
| 📂 Collapsible Sections | Hide/show command details |
| 📋 Copy Buttons | One-click command copying |
| ⚠️ Safety Notice | Highlighted privacy information |
| ❓ FAQ Section | 6 common questions answered |
| 📤 Upload Area | Drag & drop file upload |
| 🎥 Video Placeholder | Space for future tutorials |

## 📝 The 6 Steps

1. **Enable Developer Mode** - Tap Build Number 7 times
2. **Enable USB Debugging** - Turn on in Developer Options
3. **Install Platform Tools** - Download from Google
4. **Connect Phone** - USB cable + allow debugging
5. **Verify Connection** - Run `adb devices`
6. **Extract Data** - Run safe read-only commands

## 💻 Commands Provided

```bash
# Check connection
adb devices

# Apps list
adb shell pm list packages > apps.txt

# Permissions
adb shell dumpsys package > permissions.txt

# Call logs
adb shell content query --uri content://call_log/calls > calls.txt

# SMS logs
adb shell content query --uri content://sms > sms.txt
```

## 🎨 UI Elements

- **Purple gradient header** - Matches main site
- **White card sections** - Clean, organized
- **Green toggle button** - Simplified view
- **Copy buttons** - All commands
- **Yellow warning box** - Safety notice
- **Collapsible arrows** - Expand/collapse

## 🔒 Safety Guarantees

✅ Read-only extraction
✅ No rooting required
✅ No data modification
✅ Own device only
✅ Privacy preserved
✅ Legal use only

## 📊 Page Structure

```
Header (Purple)
    ↓
Simplified Toggle (Green)
    ↓
Simplified View (Hidden by default)
    ↓
Detailed View (Visible by default)
    ├── Checklist
    ├── Step 1-6 Cards
    └── Commands (Collapsible)
    ↓
Upload Section
    ↓
Safety Notice (Yellow)
    ↓
Video Placeholder
    ↓
FAQ Section
```

## 🧪 Testing

Run: `python test_extraction_guide.py`

Expected: All ✅ (11 checks pass)

## 📁 Files

- `templates/extraction_guide.html` (30KB)
- `app.py` (route added)
- `templates/index.html` (link added)

## 🎯 Target Users

- Non-technical users
- Cyber harassment victims
- Personal security enthusiasts
- Anyone analyzing their own device

## 💡 Pro Tips

1. **Use simplified view** for beginners
2. **Copy commands** don't type them
3. **Read safety notice** before starting
4. **Check FAQ** if stuck
5. **Keep USB debugging off** when done

## 🔗 Integration

**From Home Page**: Green button "📱 Extract Data from Your Android Phone"

**Direct Link**: `/extraction-guide` route

## 📈 Success Metrics

- 80% user satisfaction target
- 60% completion rate target
- 50% upload rate target
- 90% safety understanding target

## 🚨 Important Notes

⚠️ **Own device only** - Never use on someone else's phone
⚠️ **Consent required** - User must agree to extraction
⚠️ **Privacy first** - Data stays on user's computer
⚠️ **Legal use** - Personal security analysis only

## 📞 Support

**FAQ Section**: Covers 6 common issues
**Troubleshooting**: Device not detected, permissions, etc.

## 🎬 Demo Flow

1. Show home page → Click button
2. Toggle simplified view
3. Expand collapsible section
4. Click copy button
5. Show safety notice
6. Demonstrate upload area

## ⏱️ Time Required

**User Time**: 15-20 minutes
**Page Load**: <1 second
**File Size**: 30KB

## ✅ Checklist Before Use

- [ ] Android phone ready
- [ ] USB cable available
- [ ] Computer ready
- [ ] Internet connection
- [ ] 15-20 minutes available

## 🎓 Learning Curve

- **Simplified View**: 5 minutes to understand
- **Detailed View**: 10 minutes to understand
- **First Extraction**: 20 minutes
- **Subsequent Extractions**: 5 minutes

## 🌐 Browser Support

✅ Chrome/Edge (recommended)
✅ Firefox
✅ Safari
✅ Mobile browsers

## 📱 Mobile Responsive

✅ Adapts to screen size
✅ Touch-friendly buttons
✅ Readable on small screens

## 🔄 Update Frequency

**Recommended**: Quarterly
**Required**: When ADB commands change
**Optional**: Add videos, improve FAQ

## 📚 Documentation

- `EXTRACTION_GUIDE_DOCUMENTATION.md` - Full docs
- `EXTRACTION_GUIDE_SUMMARY.md` - Summary
- `EXTRACTION_GUIDE_QUICK_REF.md` - This file

---

**Quick Start**: Run `python app.py` → Open http://127.0.0.1:5000 → Click green button

**Status**: ✅ Ready for use
