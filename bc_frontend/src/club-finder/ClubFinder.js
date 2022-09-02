import RangeSlider from 'react-range-slider-input';
import {useState} from 'react'
import "./ClubFinder.css"
import { useNavigate } from 'react-router-dom'

const ClubFinder = () => {

  const [checkboxOpen, setCheckboxOpen] = useState(true)
  const [checkboxClosed, setCheckboxClosed] = useState(false)
  const [checkboxInviteOnly, setCheckboxInviteOnly] = useState(false)
  const [sliderRequiredTrophiesMaxValue, setSliderRequiredTrophiesMaxValue] = useState(15000)
  const [sliderMembersMinValue, setSliderMembersMinValue] = useState(20)
  const [sliderMembersMaxValue, setSliderMembersMaxValue] = useState(29)
  const navigate = useNavigate()

  const handleChange = (e) => {
    if (e.target.name === "type-open") {
      setCheckboxOpen(e.target.checked)
    } else if (e.target.name === "type-closed") {
      setCheckboxClosed(e.target.checked)
    } else if (e.target.name === "type-invite-only") {
      setCheckboxInviteOnly(e.target.checked)
    }
  }

  const sliderMembersHandleInput = (e) => {
    let min, max;
    [min, max] = e
    setSliderMembersMinValue(min)
    setSliderMembersMaxValue(max)
  }
  const sliderRequiredTrophiesHandleInput = (e) => {
    let max;
    [, max] = e
    setSliderRequiredTrophiesMaxValue(max)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    let get_params = "?"
    if (checkboxOpen) {
      get_params += "type=open&"
    }
    if (checkboxClosed) {
      get_params += "type=closed&"
    }
    if (checkboxInviteOnly) {
      get_params += "type=invite_only&"
    }
    get_params += `min_members=${sliderMembersMinValue}&`
    get_params += `max_members=${sliderMembersMaxValue}&`
    get_params += `max_trophies=${sliderRequiredTrophiesMaxValue}`
    navigate(`/club-finder/results/${get_params}`)
  }

  return (
    <main className='col-10 col-lg-7 Player justify-content-center'>
      <h1>Find your perfect club</h1>
      <form id="club-finder-form" method='get' action="#"
      className="d-flex flex-column" onSubmit={handleSubmit}>
        <div className="d-flex flex-column my-2">
          <p>Club with trophy requirement at most at
            <span className="controlled-value">{sliderRequiredTrophiesMaxValue}</span>
          </p>
          <RangeSlider
          id="trophy-requirement-slider"
          min={0}
          max={60000}
          step={1000}
          defaultValue={[0, sliderRequiredTrophiesMaxValue]}
          thumbsDisabled={[true, false]}
          onInput={sliderRequiredTrophiesHandleInput}
          />
        </div>
        <div className="mt-3">
          <p>Club type is :</p>
          <div className="d-flex justify-content-around">
            <article>
              <input type="checkbox" name="type-open" checked={checkboxOpen ? true : ""}
              onChange={handleChange}
              />
              <div>
                <span>Open</span>
              </div>
              <label htmlFor="type-open" className="form-check-label">Open</label>
            </article>
            <article>
              <input type="checkbox" name="type-closed"
              checked={checkboxClosed ? true : ""}
              onChange={handleChange}
              />
              <div>
                <span>Closed</span>
              </div>
              <label htmlFor="type-closed" className="form-check-label">Closed</label>
            </article>
            <article>
              <input type="checkbox" name="type-invite-only"
              checked={checkboxInviteOnly ? true : ""}
              onChange={handleChange}
              />
              <div>
                <span>Invite Only</span>
              </div>
              <label htmlFor="type-invite-only" className="form-check-label">
                Invite Only
              </label>
            </article>
          </div>
        </div>
        <div className="d-flex flex-column mx-auto my-3">
          
            {
              sliderMembersMaxValue !== sliderMembersMinValue ?
              <p>
                Clubs with between {sliderMembersMinValue} and {sliderMembersMaxValue} 
                &nbsp;members
              </p>
              :
              <p>Clubs with exactly ${sliderMembersMinValue} members</p>
            }
          
          <RangeSlider
          id="number-of-players-slider"
          min={1}
          max={30}
          defaultValue={[sliderMembersMinValue, sliderMembersMaxValue]}
          onInput={sliderMembersHandleInput}
          />
        </div>
        <button type="submit" className="btn clubfinder-btn">Search</button>


      </form>
    </main>
  )
}

export default ClubFinder