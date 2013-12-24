def exeption_handling(func):
  @wraps(func)
    def wrapper(*args, **kwds):
      while True:
        try:
          return func(*args, **kwds)
        except Exception as e:
          print "Wrapper caught error: ", e.message
        else:
          break
      return wrapper
