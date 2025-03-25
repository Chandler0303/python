let _count = 1e8


// generateId
const generateId = function(t) {
  t === void 0 && (t = 0);
  var e = new Date
    , r = e.getTime() - t;
  return _count += 1,
  "".concat(r).concat(_count)
}