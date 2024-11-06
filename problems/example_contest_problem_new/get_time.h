#pragma once

#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <iomanip>
#include <iostream>
#include <string>

struct timer {
  uint64_t total_time;
  uint64_t last_time;
  bool on;
  std::string name;
  //struct timezone tzp;

  timer(std::string name = "PBBS time", bool _start = true)
  : total_time(0), on(false), name(name) {
    if (_start) start();
  }

  uint64_t get_time() {
  //double get_time() {
    //timeval now;
    struct timespec  now;
    //gettimeofday(&now, &tzp);
    clock_gettime(CLOCK_MONOTONIC, &now);
    //return ((double) now.tv_sec) + ((double) now.tv_nsec)/1000000000.;
    return (now.tv_sec)*1000000000 + (now.tv_nsec);
  }

  void start () {
    on = 1;
    last_time = get_time();
  }

  uint64_t stop () {
    on = 0;
    uint64_t d = (get_time()-last_time);
    total_time += d;
    return d;
  }

  void reset() {
     total_time=0;
     on=0;
  }

  uint64_t get_total() {
    if (on) return total_time + get_time() - last_time;
    else return total_time;
  }

  uint64_t get_next() {
    if (!on) return 0;
    double t = get_time();
    double td = t - last_time;
    total_time += td;
    last_time = t;
    return td;
  }

  void report(uint64_t time, std::string str) {
    std::ios::fmtflags cout_settings = std::cout.flags();
    std::cout.precision(4);
    std::cout << std::fixed;
    std::cout << name << ": ";
    if (str.length() > 0)
      std::cout << str << ": ";
    std::cout << (time) << std::endl;
    std::cout.flags(cout_settings);
  }

  void total() {
    report(get_total(),"total");
    total_time = 0.0;
  }

  void reportTotal(std::string str) {
    report(get_total(), str);
  }

  void next(std::string str) {
    if (on) report(get_next(), str);
  }
};

static timer _tm;
static timer _tm2;
#define startTime() _tm.start();
#define nextTime(_string) _tm.next(_string);