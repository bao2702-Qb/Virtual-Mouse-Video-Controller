# Changelog

## [2.0.0] - 2025-11-28

### Added
- ✨ **Auto-select mode**: Tự động so sánh ML vs Rule-based và chọn chế độ tốt nhất
- 🤖 **ML-based gesture recognition**: Support 3 models (Random Forest, SVM, MLP)
- 📊 **Multi-model training**: Train tất cả models và auto-select model tốt nhất
- 🔄 **Dual-mode system**: ML-based (95%+) và Rule-based (78%) với toggle 'M'
- 📁 **Auto data collection**: Automated training data collection
- 🎯 **Model comparison tool**: So sánh accuracy giữa các modes
- ⚙️ **Config persistence**: Lưu selected mode vào model_config.json
- 📝 **Comprehensive documentation**: AUTO_SELECT_GUIDE.md, TRAINING_GUIDE.md

### Changed
- 🔧 Simplified project structure (removed redundant files)
- 📦 Updated README.md - ngắn gọn, dễ hiểu hơn
- 🎨 Improved .gitignore
- 📋 Better requirements.txt with comments

### Fixed
- ✅ Volume gesture detection (thumb LEFT + finger spread/close)
- ✅ Next_video gesture (4 fingers, exclude thumb)
- ✅ ML model loading với auto-detect
- ✅ Metadata JSON serialization
- ✅ Dynamic class handling trong training

### Removed
- ❌ run_ml.py, run_rulebased.py (consolidated into run.py)
- ❌ train_workflow.py (redundant)
- ❌ quick_compare.py (integrated into auto_select_mode.py)

## [1.0.0] - Initial Release

### Features
- Basic hand tracking với MediaPipe
- Rule-based gesture detection
- Mouse control (moving, clicking)
- Video control (forward, backward)
- Volume control
- Next video navigation
