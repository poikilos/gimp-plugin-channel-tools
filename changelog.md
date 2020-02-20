# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [git] - 2020-02-20
### Added
- diffimage.py compares two images (calls tinkerduck.py)
- ChannelTinkerProgressInterface and ChannelTinkerInterface are
  available and allow the module to contain more of the functions that
  would otherwise be dependent upon the backend (GIMP or PIL).

### Changed
- Rename plug-in to channel_tinker a.k.a. "Channel Tinker" (and module
  to channel_tinker)
- Make the channel_tinker module entirely duck-typed.
    - Move gimp-specific usages to plugin script.


## [git] - 2020-02-19
### Added
- Draw Centered Square.
