from bbb_presentation_video.renderer.tldraw.v2.utils import rng


def test_rng() -> None:
    # The same sequence as tldraw's rng in the client
    random = rng("shape:S_7PT3QSaUT6dzHcRV8Eb")
    assert random() == -0.908886041957885
    assert random() == 0.10081166634336114
    assert random() == -0.9312297338619828
