import numpy as np
import cv2
from skimage import exposure

class ImageProcess:
    DISTANCE_TOLERANCE = 0.7
    MATCHES_NUMBER_TOLERANCE = 7
    FLANN_INDEX_LSH = 6

    @classmethod
    def correctImage(self, tmpl_stream, rp_stream):
        tmpl_buf = np.asarray(bytearray(tmpl_stream.read()), dtype=np.uint8)
        rp_buf = np.asarray(bytearray(rp_stream.read()), dtype=np.uint8)
        
        tmpl_img = cv2.imdecode(tmpl_buf, cv2.IMREAD_COLOR)
        rp_img = cv2.imdecode(rp_buf, cv2.IMREAD_COLOR)

        surf = cv2.ORB_create()

        tmpl_kp, tmpl_des = surf.detectAndCompute(tmpl_img, None)
        rp_kp, rp_des = surf.detectAndCompute(rp_img, None)

        idx_parms = dict(algorithm = self.FLANN_INDEX_LSH,
                         table_number = 6,
                         key_size = 12,
                         multi_probe_level = 1)
        srch_parms = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(idx_parms, srch_parms)

        matches = flann.knnMatch(tmpl_des, rp_des, k=2)

        matches = list(filter(lambda x:len(x)==2, matches))

        good_matches = []

        for m,n in matches:
            if m.distance < self.DISTANCE_TOLERANCE * n.distance:
                good_matches.append(m)

        if len(good_matches) >= self.MATCHES_NUMBER_TOLERANCE:
            tmpl_matches_pts = np.float32([tmpl_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            rp_matches_pts = np.float32([rp_kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            homography, _ = cv2.findHomography(tmpl_matches_pts, rp_matches_pts, cv2.RANSAC, 5.0)

            h,w = tmpl_img.shape[:2]
            tmpl_corners = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)

            rp_corners = cv2.perspectiveTransform(tmpl_corners, homography)
            mask = cv2.getPerspectiveTransform(rp_corners, tmpl_corners)
            crt_img = cv2.warpPerspective(rp_img, mask, (w, h), cv2.INTER_LINEAR | cv2.WARP_FILL_OUTLIERS, cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

            crt_img = exposure.rescale_intensity(crt_img, out_range=(0, 255))

            _, crt_img_buf = cv2.imencode(".png", crt_img)

            return crt_img_buf.tostring()
        else:
            raise ArithmeticError("Couldn't find enought matches - %d(at least %d) - between template and report" %(len(good_matches), self.MATCHES_NUMBER_TOLERANCE))
            
