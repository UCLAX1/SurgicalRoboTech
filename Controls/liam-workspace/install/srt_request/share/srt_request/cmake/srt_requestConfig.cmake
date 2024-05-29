# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_srt_request_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED srt_request_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(srt_request_FOUND FALSE)
  elseif(NOT srt_request_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(srt_request_FOUND FALSE)
  endif()
  return()
endif()
set(_srt_request_CONFIG_INCLUDED TRUE)

# output package information
if(NOT srt_request_FIND_QUIETLY)
  message(STATUS "Found srt_request: 0.0.0 (${srt_request_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'srt_request' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${srt_request_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(srt_request_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${srt_request_DIR}/${_extra}")
endforeach()
